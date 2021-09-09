import docker_jenkins_utils.gitlab_common as git
import os
import shutil
from docker_jenkins_utils.common import getGitInfo
import subprocess


def createAndLoadRepo(repoName, src, branch="master", tag=None):
    git.createRepo(repoName)
    execute(["git", "init"], src)
    execute(["git", "checkout", "-b", branch], src)
    execute(["git", "add", "."], src)
    execute(["git", "commit", "-am", "'init'"], src)
    url = getGitInfo()['baseUrlWithCreds'] + "/" + repoName + ".git"
    execute(["git", "remote", "add", "origin", url], src)
    execute(["git", "push", "origin", branch], src)
    if tag is not None:
        execute(["git", "tag", tag], src)
        execute(["git", "push", "origin", tag], src)
    return getGitInfo()['baseUrl'] + "/" + repoName + ".git"


def cloneRepo(url, targetDir):
    execute(["git", "clone", url], targetDir)


def loadPipeline(dir):
    if os.path.exists("./src"):
        shutil.copytree("./src", dir.dirname + '/pipeline/src')
    if os.path.exists("./vars"):
        shutil.copytree("./vars", dir.dirname + '/pipeline/vars')
    if os.path.exists("./pipeline.groovy"):
        os.mkdir(dir.dirname + "/pipeline")
        shutil.copy("./pipeline.groovy", dir.dirname + "/pipeline/pipeline.groovy")
    createAndLoadRepo("pipeline", dir.dirname + "/pipeline", tag="DEVELOP")


def execute(command=[], path=None):
    return subprocess.check_output(command, cwd=path)
