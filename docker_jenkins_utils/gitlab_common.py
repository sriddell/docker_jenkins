from __future__ import print_function
import requests
from docker_jenkins_utils.common import gitLabUrl, getGitlabToken


def createRepo(name):
    token = getGitlabToken()
    url = gitLabUrl() + "projects"
    headers = {'PRIVATE-TOKEN': token}
    params = {'name': name, 'visibility': 'internal'}
    requests.post(url, headers=headers, params=params)


def addSshKey(key):
    token = getGitlabToken()
    url = gitLabUrl() + "user/keys"
    headers = {'PRIVATE-TOKEN': token}
    params = {'title': 'main', 'key': key}
    print(url)
    print(requests.post(url, headers=headers, params=params))


def getRepos():
    token = getGitlabToken()
    url = gitLabUrl()
    headers = {'PRIVATE-TOKEN': token}
    url = url + "projects"
    resp = requests.get(url, headers=headers)
    return resp.json()


def deleteRepos():
    repos = getRepos()
    for repo in repos:
        token = getGitlabToken()
        url = gitLabUrl()
        headers = {'PRIVATE-TOKEN': token}
        url = url + "projects/" + str(repo['id'])
        requests.delete(url, headers=headers)
