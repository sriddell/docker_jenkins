from __future__ import print_function
import requests

from docker_jenkins_utils.common import getGitServer











def getRepos():
    url = getGitServer().externalGitUrl()
    headers = {'accept': 'application/json'}
    url = url + "repos/search"
    resp = requests.get(url, auth=getBasicAuth(), headers=headers)
    if resp.status_code != 200:
        raise Exception("getRepos:" + str(resp.status_code) + ' ' + resp.text)
    return resp.json()


def deleteRepos():
    repos = getRepos()
    for repo in repos['data']:
        url = getGitServer().externalGitUrl()
        url = url + "repos/" + str(repo['owner']['login']) + '/' + repo['name']
        headers = {'accept': 'application/json'}
        resp = requests.delete(url, auth=getBasicAuth(), headers=headers)
        if resp.status_code != 204:
            raise Exception("deleteRepos:" + str(resp.status_code) + ' ' + resp.text)
