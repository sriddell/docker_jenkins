import subprocess
import sys
import requests
import os
import time
import boto3

DOCKER_HOST_ADDR = None


def checkHealth(service, port="3000", path="/health"):
    port = getContainerPort(service, port)
    url = "http://" + getDockerHostAddr() + ":" + port + path
    healthy = False
    count = 0
    print("Checking for health of " + service + " at " + url)
    sys.stdout.flush()
    maxRetries = 40
    while not healthy and count < maxRetries:
        time.sleep(min(5, count))
        count = count + 1
        try:
            r = requests.get(url)
            if r.status_code == 200 or r.status_code == 204 or r.status_code == 403:
                healthy = True
        except requests.ConnectionError:
            pass
        if not healthy and count < maxRetries:
            print("...not healthy, waiting " + str(min(5, count)) + " seconds to try again; " + str(maxRetries - count) + " tries left")
            sys.stdout.flush()
    if not healthy:
        print("Service " + service + " failed to become healthy")
        sys.stdout.flush()
        sys.exit(1)
    else:
        print(service + " is healthy")
        sys.stdout.flush()


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
    global DOCKER_HOST_ADDR
    if DOCKER_HOST_ADDR is None:
        DOCKER_HOST_ADDR = os.environ.get('DOCKER_HOST_ADDR')
        if DOCKER_HOST_ADDR is None:
            try:
                output = check_output(["docker-machine", "active"]).strip()
                DOCKER_HOST_ADDR = check_output(["docker-machine", "ip", output]).strip()
            except (OSError, subprocess.CalledProcessError):
                # We will reach this branch if the "docker-machine" command does not
                # exist or if "docker-machine active" exits with an error status
                import socket
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 53))
                addr = s.getsockname()[0]
                s.close()
                DOCKER_HOST_ADDR = addr
    return DOCKER_HOST_ADDR


def getContainerPort(service, port="3000"):
    output = check_output(['docker-compose', 'port', service, str(port)])
    return output.split(':')[1].strip()


def execute(command=[]):
    print("executing " + command)
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    dir_path = os.path.abspath(dir_path + '/..')
    print("executing in path " + dir_path)
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
        raise subprocess.CalledProcessError(exitCode, command, output)


def aws_put_secure_string(name, value):
    client = boto3.client('ssm', endpoint_url=awsEndpointUrl(), region_name='us-east-1')
    client.put_parameter(
        Name=name,
        Value=value,
        Type='SecureString',
        Overwrite=True
    )


def aws_create_s3_bucket(name):
    client = boto3.client('s3', endpoint_url=awsEndpointUrl(), region_name='us-east-1')
    client.create_bucket(
        ACL='private',
        Bucket=name
    )


def aws_put_secrets_manager_string(name, value):
    client = boto3.client('secretsmanager', endpoint_url=awsEndpointUrl(), region_name='us-east-1')
    client.create_secret(
        Name=name,
        SecretString=value,
        ForceOverwriteReplicaSecret=True
    )


def reset_verdaccio():
    execute("docker-compose kill verdaccio")
    execute("docker-compose rm -f verdaccio")
    execute("docker-compose up -d verdaccio")
    checkHealth("verdaccio", "4873", "")


def reset_aws():
    execute("docker-compose kill aws")
    execute("docker-compose rm -f aws")
    execute("docker-compose up -d aws")
    checkHealth("aws", "4566")


def getGitlabToken():
    # This is now created during gitlab startup via the gitlab_init.rb file
    return 'skfj2348yrhauewsdfisa'


def gitLabUrl():
    url = "http://" + getDockerHostAddr() + ":" + getContainerPort("gitlab", 80) + "/api/v4/"
    return url


def getGitInfo():
    info = {}
    info['baseUrlWithCreds'] = "http://root:password@" + getDockerHostAddr() + ":" + getContainerPort("gitlab", 80) + "/root"
    info['baseUrl'] = "http://" + getDockerHostAddr() + ":" + getContainerPort("gitlab", 80) + "/root"
    return info


def jenkinsUrl():
    return "http://admin:admin@" + getDockerHostAddr() + ":" + getContainerPort("jenkins", 8080) + "/"


def verdaccioUrl():
    return "http://" + getDockerHostAddr() + ":" + getContainerPort("verdaccio", 4873)


def awsEndpointUrl():
    return "http://" + getDockerHostAddr() + ":" + getContainerPort("aws", 4566)
