from __future__ import print_function
import requests
from requests.auth import HTTPBasicAuth
from docker_jenkins_utils.common import gitUrl, getGitlabToken


def getBasicAuth():
    return HTTPBasicAuth('root', 'admin')


def createRepo(name):
    url = gitUrl() + "user/repos"
    payload = '''{
        "auto_init": false,
        "default_branch": "master",
        "name": "''' + name + '''",
        "private": false,
        "trust_model": "default"
    }'''
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    resp = requests.post(url=url, headers=headers, auth=getBasicAuth(), data=payload)
    if resp.status_code != 201:
        raise Exception("createRepo:" + str(resp.status_code) + ' ' + resp.text)


def addSshKey(key, repo):
    url = gitUrl() + "repos/root/" + repo + "/keys"
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    payload = '''{
        "key": "''' + key + '''",
        "read_only": false,
        "title": "gitops"
    }'''
    resp = requests.post(url=url, headers=headers, auth=getBasicAuth(), data=payload)
    if resp.status_code != 201:
        raise Exception("createRepo:" + str(resp.status_code) + ' ' + resp.text)


def getRepos():
    url = gitUrl()
    headers = {'accept': 'application/json'}
    url = url + "repos/search"
    resp = requests.get(url, auth=getBasicAuth(), headers=headers)
    if resp.status_code != 200:
        raise Exception("getRepos:" + str(resp.status_code) + ' ' + resp.text)
    return resp.json()


def deleteRepos():
    repos = getRepos()
    for repo in repos['data']:
        print(repo)
        url = gitUrl()
        url = url + "repos/" + str(repo['owner']['login']) + '/' + repo['name']
        headers = {'accept': 'application/json'}
        resp = requests.delete(url, auth=getBasicAuth(), headers=headers)
        if resp.status_code != 204:
            raise Exception("deleteRepos:" + str(resp.status_code) + ' ' + resp.text)
