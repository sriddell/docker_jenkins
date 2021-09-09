from __future__ import print_function
import os
import time
import calendar
import sys
import shutil
from docker_jenkins_utils.common import checkHealth, getDockerHostAddr, execute, reset_verdaccio

# main cmd options
if not os.path.exists('build'):
    os.makedirs('build')
if os.path.exists("../plugins.txt"):
    shutil.copyfile('../plugins.txt', 'build/plugins.txt')
if os.path.exists("../testing/plugins.txt"):
    shutil.copyfile('../testing/plugins.txt', 'build/plugins.txt')
else:
    with open("build/plugins.txt", 'a'):
        os.utime("build/plugins.txt", None)


if len(sys.argv) > 1:
    if sys.argv[1] == 'all':
        cmd = "docker-compose build --build-arg CACHEBUST=" + str(calendar.timegm(time.gmtime())) + " --build-arg DOCKER_HOST_ADDR=" + str(getDockerHostAddr()) + " jenkins"
        execute(cmd)
        execute("docker-compose up -d")
    if sys.argv[1] == 'reset-verdaccio':
        reset_verdaccio()


checkHealth("jenkins", "8080", "")
checkHealth("verdaccio", "4873", "")
checkHealth("artifactory", "8081", "")
checkHealth("gitlab", "80", "")
checkHealth("aws", "4566")

execute("docker-compose exec gitlab gitlab-rails runner /gitlab_init.rb")
