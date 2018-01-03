import docker_jenkins.gitlab_common as git
import os
import shutil
from common import getGitInfo
import subprocess

def createAndLoadRepo(repoName, src, branch="master", tag=None):
    git.createRepo(repoName)
    execute(["git", "init"], src)
    execute(["git", "checkout", "-b", branch], src)
    execute(["git", "add", "."], src)
    execute(["git", "commit", "-am", "'init'"], src)
    url = getGitInfo()['baseUrl'] + "/" + repoName + ".git"
    execute(["git", "remote", "add", "origin", url], src)
    execute(["git", "push", "origin", branch], src)
    if tag != None:
        execute(["git", "tag", tag], src)
        execute(["git", "push", "origin", tag], src)
    return url

def loadPipeline(dir):
    os.mkdir(dir.dirname + "/pipeline")
    shutil.copy("./pipeline.groovy", dir.dirname + "/pipeline")
    createAndLoadRepo("pipeline", dir.dirname + "/pipeline", tag="DEVELOP")

def execute(command = [], path=None):
    return subprocess.check_output(command, cwd=path)