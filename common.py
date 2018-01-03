import subprocess
import sys
import requests
import json
import os

def check_output(*args, **kwargs):
    path = os.path.dirname(__file__)
    result = subprocess.check_output(*args, cwd=path, **kwargs)
    if sys.version_info >= (3, 0):
        # Under Python 3, the output of subprocess.check_output is a "bytes"
        # object, which must be decoded if we want to treat it as a string
        return result.decode('utf-8')
    else:
        return result

def getDockerHostAddr():
    try:
        output = check_output(["docker-machine", "active"]).strip()
        return check_output(["docker-machine", "ip", output]).strip()
    except (OSError, subprocess.CalledProcessError):
        # We will reach this branch if the "docker-machine" command does not
        # exist or if "docker-machine active" exits with an error status
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",53))
        addr = s.getsockname()[0]
        s.close()
        return addr

def getContainerPort(service, port="3000"):
    output = check_output(["docker-compose", "port", service, str(port)])
    return output.split(":")[1].strip()

def getGitlabToken():
    port = getContainerPort("gitlab", "80")
    url = "http://" + getDockerHostAddr() + ":" + port + "/api/v3/session?login=root&password=password"
    resp = requests.post(url)
    j = json.loads(resp.text)
    return j['private_token']

def gitLabUrl():
    url = "http://" + getDockerHostAddr() + ":" + getContainerPort("gitlab", 80) + "/api/v3/"
    return url

def getGitInfo():
    info = {}
    info['baseUrl'] = "http://root:password@" + getDockerHostAddr() + ":" + getContainerPort("gitlab", 80) + "/root"
    return info

def jenkinsUrl():
    return "http://admin:admin@" + getDockerHostAddr() + ":" + getContainerPort("jenkins", 8080) + "/"

def verdaccioUrl():
    return "http://" + getDockerHostAddr() + ":" + getContainerPort("verdaccio", 4873)