from docker_jenkins_utils.common import getGitServer
import os
import shutil
from docker_jenkins_utils.common import getGitServer
import subprocess



def createAndLoadRepo(repoName, src, branch="master", tag=None):
    url = getGitServer().createRepo(repoName)
    execute(["git", "init"], src)
    execute(["git", "checkout", "-b", branch], src)
    execute(["git", "add", "."], src)
    execute(["git", "commit", "-am", "'init'"], src)
    print('>>>>>>>>>>>>>>')
    print(url)
    execute(["git", "remote", "add", "origin", url], src)
    execute(["git", "push", "origin", branch], src)
    if tag is not None:
        execute(["git", "tag", tag], src)
        execute(["git", "push", "origin", tag], src)
    return getGitServer().internalGitUrl(repoName)


def cloneRepo(url, targetDir):
    execute(["git", "clone", url], targetDir)


def loadPipeline(dir):
    if os.path.exists("./src"):
        shutil.copytree("./src", dir + '/pipeline/src')
    if os.path.exists("./vars"):
        shutil.copytree("./vars", dir + '/pipeline/vars')
    if os.path.exists("./pipeline.groovy"):
        os.mkdir(dir + "/pipeline")
        shutil.copy("./pipeline.groovy", dir + "/pipeline/pipeline.groovy")
    createAndLoadRepo("pipeline", dir + "/pipeline", tag="DEVELOP")


def execute(command=[], path=None):
    return subprocess.check_output(command, cwd=path)
