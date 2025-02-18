from __future__ import print_function
import requests
from docker_jenkins_utils import common
from docker_jenkins_utils.common import execute
from jinja2 import Environment, FileSystemLoader
import os
import json
import time
import urllib
import jenkins


def addJob(folder_name, job_name, repoUrl):
    result = prepareSession()
    session = result['session']
    headers = result['headers']
    thisDir = os.path.dirname(os.path.abspath(__file__))
    j2 = Environment(loader=FileSystemLoader(thisDir), trim_blocks=True)
    content = j2.get_template('templates/config.xml').render(name=job_name, repo_url=repoUrl)
    headers.update({"Content-Type": "text/xml; charset=UTF-8"})
    url = common.jenkinsUrl() + 'job/' + folder_name + '/createItem?name=' + job_name
    r = session.post(url, data=content, headers=headers)
    if r.status_code != 200:
        raise Exception("Failed to add job; status was " + str(r.status_code))

def createFolder(name):
    try:
        server = jenkins.Jenkins(common.jenkinsUrl(), username='admin', password='admin')
        server.create_job(name, jenkins.EMPTY_FOLDER_XML)
    except jenkins.JenkinsException as e:
        print("Have jenkins exception")
        print(e)


def addPipelineJob(folder_name, job_name, repoUrl, directory):
    result = prepareSession()
    session = result['session']
    headers = result['headers']
    thisDir = os.path.dirname(os.path.abspath(__file__))
    j2 = Environment(loader=FileSystemLoader(thisDir), trim_blocks=True)
    content = j2.get_template('templates/pipeline.xml').render(name=job_name, repo_url=repoUrl, directory=directory)
    headers.update({"Content-Type": "text/xml; charset=UTF-8"})
    url = common.jenkinsUrl() + 'job/' + folder_name + '/createItem?name=' + job_name
    r = session.post(url, data=content, headers=headers)
    if r.status_code != 200:
        raise Exception("Failed to add job; status was " + str(r.status_code))


def runJob(folder, name, branch='master'):
    result = prepareSession()
    session = result['session']
    headers = result['headers']
    url = common.jenkinsUrl() + "job/" + folder +  "/job/" + name + "/job/" + branch + "/build?delay=0sec"
    print("running job=" + url)
    r = session.post(url, headers=headers)
    if r.status_code != 201:
        raise Exception("Failed to start job " + url + "; status was " + str(r.status_code))


def waitForBuild(folder, job, branch=None, build_number=1):
    # print('>>>> waiting for ' + folder + '/' + job + '/job/' + branch + '/' + str(build_number))
    buildId = waitForBuildToExist(folder, job, branch, build_number)
    # print(">>>>> buildId=" + str(buildId))
    if buildId is None:
        return None
    status = -1
    count = 900
    url = None
    if branch is not None:
        url = common.jenkinsUrl() + "job/" + folder + '/job/' + job + "/job/" + branch + "/" + str(buildId) + "/api/json"
    else:
        url = common.jenkinsUrl() + "job/" + folder + '/job/' + job + "/" + str(buildId) + "/api/json"
    # print(">>>>>> waiting: " + url)
    while status != 200 and count >= 0:
        count = count - 1
        resp = requests.get(url)
        status = resp.status_code
        if status == 200:
            # print(resp.text)
            j = json.loads(resp.text)
            if j['building'] is False:
                return j
            else:
                status = -1
                time.sleep(1)
    return None


def getConsole(folder_name, job, branch, buildId):

    result = prepareSession()
    session = result['session']
    headers = result['headers']
    url = None
    if branch is not None:
        url = common.jenkinsUrl() + "job/" + folder_name + "/job/" + job + "/job/" + branch + "/" + str(buildId) + "/consoleText"
    else:
        url = common.jenkinsUrl() + "job/" + folder_name + "/job/" + job + "/" + str(buildId) + "/consoleText"
    print("getConsole url=" + url)
    resp = session.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.text
    else:
        raise Exception("Failed to retrieve console for " + url + ': ' + str(resp.status_code))


def getArtifact(folder_name, job, branch, buildId, relativePath):
    url = common.jenkinsUrl() + "job/" + folder_name + "/job/" + job + "/job/" + branch + "/" + str(buildId) + "/artifact/" + relativePath
    print(url)
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("Failed to retrieve artifact " + str(resp.status_code))
    return resp.text


# def proceed(job, branch, buildId, inputId):
#     url = common.jenkinsUrl() + "job/" + job + "/job/" + branch + "/" + str(buildId) + "/input/" + inputId + "/proceedEmpty"
#     resp = requests.post(url)
#     if resp.status_code != 200:
#         raise Exception("Failed to proceed" + str(resp.status_code))
#     return resp.text


# def abort(job, branch, buildId, inputId):
#     url = common.jenkinsUrl() + "job/" + job + "/job/" + branch + "/" + str(buildId) + "/input/" + inputId + "/abort"
#     resp = requests.post(url)
#     if resp.status_code != 200:
#         raise Exception("Failed to abort" + str(resp.status_code))
#     return resp.text


def waitForBuildToExist(folder, job, branch=None, build_number=1):
    build_number=int(build_number)
    status = -1
    count = 60
    url = None
    if branch is not None:
        url = common.jenkinsUrl() + "job/" + folder + '/job/' + job + "/job/" + branch + "/api/json"
    else:
        url = common.jenkinsUrl() + "job/" + folder + '/job/' + job + "/api/json"
    while status != 200 and count >= 0:
        count = count - 1
        resp = requests.get(url)
        status = resp.status_code
        if status == 200:
            # print('>>>>response for build check of ' + url)
            # print(resp.text)
            j = json.loads(resp.text)
            for b in j['builds']:
                if b['number'] == build_number:
                    return b['number']
        status = -1
        time.sleep(1)
    return None


def scanMultibranchPipeline(folder_name, job):
    result = prepareSession()
    session = result['session']
    headers = result['headers']
    r = session.post(common.jenkinsUrl() + "job/" + folder_name + "/job/" + job + "/build?delay=0", headers=headers)
    if r.status_code != 200:
        raise Exception("Failed scan multibranch pipeline " + str(r.status_code))


def runPipeline(folder_name, job):
    result = prepareSession()
    session = result['session']
    headers = result['headers']
    r = session.post(common.jenkinsUrl() + "job/" + folder_name + "/job/" + job + "/build?delay=0", headers=headers)
    if r.status_code != 201:
        raise Exception("Failed to run pipeline " + str(r.status_code))
    

def deleteBuild(folder_name, job, branch="master", number="1"):
    result = prepareSession()
    session = result['session']
    headers = result['headers']
    url = common.jenkinsUrl() + "job/" + folder_name, + "/job/" + job + "/job/" + branch + "/" + number + "/doDelete"
    print("delete=" + url)
    r = session.post(url, headers=headers)
    if r.status_code != 200:
        raise Exception("Failed to delete build " + str(r.status_code))


def addUsernamePasswordCredential(id, username, password):
    template = """
import com.cloudbees.plugins.credentials.impl.*;
import com.cloudbees.plugins.credentials.*;
import com.cloudbees.plugins.credentials.domains.*;
Credentials c = (Credentials) new 'UsernamePasswordCredentialsImpl'(CredentialsScope.GLOBAL,"{0}", "description", "{1}", "{2}")
SystemCredentialsProvider.getInstance().getStore().addCredentials(Domain.global(), c)
"""
    executeScript(template.format(id, username, password))


def addSshUser(id, username, privateKeyString):
    template = '''
import com.cloudbees.plugins.credentials.impl.*;
import com.cloudbees.plugins.credentials.*;
import com.cloudbees.plugins.credentials.domains.*;
import com.cloudbees.jenkins.plugins.sshcredentials.impl.*;
key = """''' + privateKeyString + '''"""
BasicSSHUserPrivateKey.DirectEntryPrivateKeySource source = new BasicSSHUserPrivateKey.DirectEntryPrivateKeySource(key)
Credentials c = (Credentials) new BasicSSHUserPrivateKey(CredentialsScope.GLOBAL,"{0}", "{1}", source, "", "description")
SystemCredentialsProvider.getInstance().getStore().addCredentials(Domain.global(), c)
'''

    executeScript(template.format(id, username))


def clearAllJobs():
    template = """
import hudson.matrix.*
import jenkins.model.*;
import com.cloudbees.hudson.plugins.folder.*
while (Jenkins.getInstance().getAllItems().size() > 0) {
    Jenkins.getInstance().getAllItems()[0].delete()
}
"""
    executeScript(template)


# def createFolder(name):
#     template= '''
# Jenkins.instance.createProject(com.cloudbees.hudson.plugins.folder.Folder.class, "''' + name + '''")
# '''    


def addEnvVars(values):
    s = '''
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
'''
    for k, v in values.items():
        s += 'envVars.put("' + k + '", "' + v + '")\n'

    s += '''
    instance.save()
    '''
    executeScript(s)


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
    executeScript(template)


def addSecuritySignatures(sigs):
    s = '''import org.jenkinsci.plugins.scriptsecurity.scripts.*
    ScriptApproval.PendingSignature s = null
    ScriptApproval sa = null
'''
    for sig in sigs:
        s = s + '''
 signature = "''' + sig + '''"
 s = new ScriptApproval.PendingSignature(signature, false, ApprovalContext.create())

  sa = ScriptApproval.get();
  sa.approveSignature(s.signature);
'''
    executeScript(s)


def executeScript(script):
    result = prepareSession()
    session = result['session']
    headers = result['headers']
    headers.update({"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
    print('executing jenkins script using ' + common.jenkinsUrl())
    r = session.post(common.jenkinsUrl() + "scriptText", data={'script': script}, headers=headers)

    if r.status_code != 200:
        raise Exception("Failed to run script " + script)


def prepareSession():
    # Build the Jenkins crumb issuer URL
    session = requests.session()
    parsed_url = urllib.parse.urlparse(common.jenkinsUrl())
    crumb_issuer_url = urllib.parse.urlunparse((parsed_url.scheme,
                                                parsed_url.netloc,
                                                'crumbIssuer/api/json',
                                                '', '', ''))

    # Get the Jenkins crumb
    auth = requests.auth.HTTPBasicAuth('admin', 'admin')
    r = session.get(crumb_issuer_url, auth=auth)
    json = r.json()
    crumb = {json['crumbRequestField']: json['crumb']}
    headers = {}
    headers.update(crumb)
    return {
        'session': session,
        'headers': headers
    }


def clearGitConfig():
    execute("docker compose exec -T jenkins rm -f /var/jenkins_home/.gitconfig")


def clearAll():
    clearEnvVars()
    clearAllJobs()
    clearGitConfig()
