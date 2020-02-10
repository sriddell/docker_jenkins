from __future__ import print_function
import requests
from docker_jenkins_utils import common
from jinja2 import Environment, FileSystemLoader
import os
import json
import time


def addJob(name, repoUrl):
    thisDir = os.path.dirname(os.path.abspath(__file__))
    j2 = Environment(loader=FileSystemLoader(thisDir), trim_blocks=True)
    content = j2.get_template('templates/config.xml').render(name=name, repo_url=repoUrl)
    headers = {"Content-Type": "text/xml; charset=UTF-8"}
    r = requests.post(common.jenkinsUrl() + "createItem?name=" + name, data=content, headers=headers)
    if r.status_code != 200:
        raise Exception("Failed to add job; status was " + str(r.status_code))


def addPipelineJob(name, repoUrl, properties_content):
    thisDir = os.path.dirname(os.path.abspath(__file__))
    j2 = Environment(loader=FileSystemLoader(thisDir), trim_blocks=True)
    content = j2.get_template('templates/pipeline.xml').render(name=name, repo_url=repoUrl, properties_content=properties_content)
    headers = {"Content-Type": "text/xml; charset=UTF-8"}
    r = requests.post(common.jenkinsUrl() + "createItem?name=" + name, data=content, headers=headers)
    if r.status_code != 200:
        raise Exception("Failed to add job; status was " + str(r.status_code))


def runJob(job, branch):
    requests.post(common.jenkinsUrl() + "job/" + job + "/job/" + branch + "/build?delay=0sec")


def waitForBuild(job, branch=None):
    buildId = waitForBuildToExist(job, branch)
    if buildId is None:
        return None
    status = -1
    count = 900
    url = None
    if branch is not None:
        url = common.jenkinsUrl() + "job/" + job + "/job/" + branch + "/" + str(buildId) + "/api/json"
    else:
        url = common.jenkinsUrl() + "job/" + job + "/" + str(buildId) + "/api/json"
    while status != 200 and count >= 0:
        count = count - 1
        resp = requests.get(url)
        status = resp.status_code
        if status == 200:
            j = json.loads(resp.text)
            if j['building'] is False:
                return j
            else:
                status = -1
                time.sleep(1)
    return None


def getConsole(job, branch, buildId):
    url = None
    if branch is not None:
        url = common.jenkinsUrl() + "job/" + job + "/job/" + branch + "/" + str(buildId) + "/console"
    else:
        url = common.jenkinsUrl() + "job/" + job + "/" + str(buildId) + "/console"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.text
    else:
        raise Exception("Failed to retrieve console " + str(resp.status_code))


def getArtifact(job, branch, buildId, relativePath):
    print(common.jenkinsUrl() + "job/" + job + "/job/" + branch + "/" + str(buildId) + "/artifact/" + relativePath)
    resp = requests.get(common.jenkinsUrl() + "job/" + job + "/job/" + branch + "/" + str(buildId) + "/artifact/" + relativePath)
    if resp.status_code != 200:
        raise Exception("Failed to retrieve artifact " + str(resp.status_code))
    return resp.text


def proceed(job, branch, buildId, inputId):
    url = common.jenkinsUrl() + "job/" + job + "/job/" + branch + "/" + str(buildId) + "/input/" + inputId + "/proceedEmpty"
    print(url)
    resp = requests.post(url)
    if resp.status_code != 200:
        raise Exception("Failed to proceed" + str(resp.status_code))
    return resp.text


def abort(job, branch, buildId, inputId):
    url = common.jenkinsUrl() + "job/" + job + "/job/" + branch + "/" + str(buildId) + "/input/" + inputId + "/abort"
    print(url)
    resp = requests.post(url)
    if resp.status_code != 200:
        raise Exception("Failed to abort" + str(resp.status_code))
    return resp.text


def waitForBuildToExist(job, branch=None):
    status = -1
    count = 60
    url = None
    if branch is not None:
        url = common.jenkinsUrl() + "job/" + job + "/job/" + branch + "/api/json"
    else:
        url = common.jenkinsUrl() + "job/" + job + "/api/json"
    while status != 200 and count >= 0:
        count = count - 1
        resp = requests.get(url)
        status = resp.status_code
        if status == 200:
            j = json.loads(resp.text)
            if len(j['builds']) == 0:
                status = -1
                time.sleep(1)
            else:
                return j['builds'][0]['number']
    return None


def scanMultibranchPipeline(job):
    r = requests.post(common.jenkinsUrl() + "job/" + job + "/build?delay=0")
    if r.status_code != 200:
        raise Exception("Failed scan multibranch pipeline " + str(r.status_code))


def runPipeline(job):
    r = requests.post(common.jenkinsUrl() + "job/" + job + "/build?delay=0")
    if r.status_code != 201:
        raise Exception("Failed to run pipeline " + str(r.status_code))


def addUsernamePasswordCredential(id, username, password):
    template = """
import com.cloudbees.plugins.credentials.impl.*;
import com.cloudbees.plugins.credentials.*;
import com.cloudbees.plugins.credentials.domains.*;
Credentials c = (Credentials) new UsernamePasswordCredentialsImpl(CredentialsScope.GLOBAL,"{0}", "description", "{1}", "{2}")
SystemCredentialsProvider.getInstance().getStore().addCredentials(Domain.global(), c)
"""

    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    r = requests.post(common.jenkinsUrl() + "scriptText", data={'script': template.format(id, username, password)}, headers=headers)
    if r.status_code != 200:
        raise Exception("Failed to set credential; status was " + str(r.status_code))


def clearAllJobs():
    template = """
import hudson.matrix.*
import jenkins.model.*;
import com.cloudbees.hudson.plugins.folder.*
while (Jenkins.getInstance().getAllItems().size() > 0) {
    Jenkins.getInstance().getAllItems()[0].delete()
}
"""
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    r = requests.post(common.jenkinsUrl() + "scriptText", data={'script': template}, headers=headers)
    if r.status_code != 200:
        raise Exception("Failed to clear all jobs; status was " + str(r.status_code))


def addEnvVar(name, value):
    template = """
import hudson.slaves.EnvironmentVariablesNodeProperty
import jenkins.model.Jenkins

instance = Jenkins.getInstance()
globalNodeProperties = instance.getGlobalNodeProperties()
envVarsNodePropertyList = globalNodeProperties.getAll(EnvironmentVariablesNodeProperty.class)

newEnvVarsNodeProperty = null
envVars = null

if ( envVarsNodePropertyList == null || envVarsNodePropertyList.size() == 0 ) {{
  newEnvVarsNodeProperty = new EnvironmentVariablesNodeProperty();
  globalNodeProperties.add(newEnvVarsNodeProperty)
  envVars = newEnvVarsNodeProperty.getEnvVars()
}} else {{
  envVars = envVarsNodePropertyList.get(0).getEnvVars()
}}

envVars.put("{0}", "{1}")

instance.save()
"""
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    r = requests.post(common.jenkinsUrl() + "scriptText", data={'script': template.format(name, value)}, headers=headers)
    if r.status_code != 200:
        raise Exception("Failed to set env var; status was " + str(r.status_code))


def clearEnvVars():
    template = """
import hudson.slaves.EnvironmentVariablesNodeProperty
import jenkins.model.Jenkins

instance = Jenkins.getInstance()
globalNodeProperties = instance.getGlobalNodeProperties()
envVarsNodePropertyList = globalNodeProperties.getAll(EnvironmentVariablesNodeProperty.class)

newEnvVarsNodeProperty = null
envVars = null

if ( envVarsNodePropertyList == null || envVarsNodePropertyList.size() == 0 ) {
  newEnvVarsNodeProperty = new EnvironmentVariablesNodeProperty();
  globalNodeProperties.add(newEnvVarsNodeProperty)
  envVars = newEnvVarsNodeProperty.getEnvVars()
} else {
  envVars = envVarsNodePropertyList.get(0).getEnvVars()
}

envVars.clear()

instance.save()
"""
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    r = requests.post(common.jenkinsUrl() + "scriptText", data={'script': template}, headers=headers)
    if r.status_code != 200:
        raise Exception("Failed to clear all env vars; status was " + str(r.status_code))


def addSecuritySignature(sig):
    thisDir = os.path.dirname(os.path.abspath(__file__))
    j2 = Environment(loader=FileSystemLoader(thisDir), trim_blocks=True)
    script = j2.get_template('templates/addSecuritySignature.groovy').render(signature=sig)
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    r = requests.post(common.jenkinsUrl() + "scriptText", data={'script': script}, headers=headers)
    if r.status_code != 200:
        raise Exception("Failed to add security signatures; status was " + str(r.status_code))


def clearAll():
    clearEnvVars()
    clearAllJobs()
