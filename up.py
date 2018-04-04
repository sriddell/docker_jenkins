from __future__ import print_function
import os
import subprocess
import requests
import time
import calendar
import sys
import shutil
from common import getDockerHostAddr, getContainerPort


DOCKER_HOST_ADDR = os.environ.get('DOCKER_HOST_ADDR')
if DOCKER_HOST_ADDR == None:
    DOCKER_HOST_ADDR = getDockerHostAddr();

print("Using DOCKER_HOST_ADDR {0}".format(DOCKER_HOST_ADDR))
sys.stdout.flush()


def checkHealth(service, port="3000", path="/health"):
    port = getContainerPort(service, port)
    url="http://" + DOCKER_HOST_ADDR + ":" + port + path
    healthy = False
    count = 0
    print("Checking for health of " + service + " at " + url)
    sys.stdout.flush()
    maxRetries = 40
    while not healthy and count < maxRetries:
        time.sleep(min(5,count))
        count = count+1
        try:
            r = requests.get(url)
            if r.status_code == 200 or r.status_code == 204 or r.status_code == 403:
                healthy = True
        except requests.ConnectionError:
            pass
        if not healthy and count < maxRetries:
            print("...not healthy, waiting " + str(min(5,count)) + " seconds to try again; " + str(maxRetries-count) + " tries left")
            sys.stdout.flush()
    if not healthy:
        print("Service " + service + " failed to become healthy")
        sys.stdout.flush()
        sys.exit(1)
    else:
        print(service + " is healthy")
        sys.stdout.flush()

def execute(command = []):
    print(command)
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    process = subprocess.Popen(command, cwd=dir_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()
        if nextline.decode('utf-8') == '' and process.poll() is not None:
            break
        print(nextline.decode("utf-8"))
        sys.stdout.flush()

    output = process.communicate()[0]
    exitCode = process.returncode

    if (exitCode == 0):
        return output
    else:
        raise subprocess.ProcessException(command, exitCode, output)

# main cmd options
if not os.path.exists('build'):
    os.makedirs('build')
if os.path.exists("../plugins.txt"):
    shutil.copyfile('../plugins.txt', 'build/plugins.txt')
else:
    with open("build/plugins.txt", 'a'):
        os.utime("build/plugins.txt", None)

def reset_verdaccio():
    execute("docker-compose kill verdaccio")
    execute("docker-compose rm -f verdaccio")
    execute("docker-compose up -d verdaccio")
    checkHealth("verdaccio", "4873", "")

def reset_s3():
    execute("docker-compose kill s3")
    execute("docker-compose rm -f s3")
    execute("docker-compose up -d s3")
    checkHealth("s3", "80", "")

if len(sys.argv) > 1:
    if sys.argv[1] == 'all':
        cmd = "docker-compose build --build-arg CACHEBUST=" + str(calendar.timegm(time.gmtime())) + " --build-arg DOCKER_HOST_ADDR=" + str(DOCKER_HOST_ADDR) + " jenkins"
        execute(cmd)
        execute("docker-compose up -d")
    if sys.argv[1] == 'reset-verdaccio':
        reset_verdaccio()


checkHealth("jenkins", "8080", "")
checkHealth("verdaccio", "4873", "")
checkHealth("artifactory", "8081", "")
checkHealth("gitlab", "80", "")
checkHealth("s3", "80", "")




