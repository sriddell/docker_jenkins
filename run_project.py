# Script to use docker_jenkins, the dockerized jenkins local environment to load a specified directory
# containing a Jenksinfile and automatically run it.
# To use, do the following
# 1. create a new git project and add this file to it
# 2. Add the docker_jenkins git submodule 'git submodule add https://github.com/sriddell/docker_jenkins.git'
# 3. Copy the plugins.txt file defining the plugins that should be loaded into jenkins to your project root.
# For DSL Jenkinsfile development, the follow list is recommended as a starting point:
#
import docker_jenkins_utils.jenkins_common as jenkins
import docker_jenkins_utils.test_utils as test_utils
import docker_jenkins_utils.gitlab_common as git
import shutil
import os
import sys
from dotenv import dotenv_values
env = dotenv_values()

source = sys.argv[1]

tmpdir = os.path.dirname(os.path.realpath(__file__)) + '/tmp'
if os.path.exists(tmpdir):
    shutil.rmtree(tmpdir)
    os.mkdir(tmpdir)
git.deleteRepos()
jenkins.clearAll()

for key in env:
    jenkins.addEnvVar(key, env[key])

target = tmpdir + '/project'
shutil.copytree(source, target)
url = test_utils.createAndLoadRepo('project', target)
jenkins.addJob('project', url)
jenkins.scanMultibranchPipeline('project')
jenkins.waitForBuild('project', 'master')
