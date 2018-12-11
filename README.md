#Experimental jenkins image for testing pipelines-as-code

##Overview

Builds jenkins into a container along with the workflow-aggregator plugin (for pipelines as code).  Based on the build for the official Jenkins docker image (https://github.com/jenkinsci/docker).

Also sets the docker group ID to match that in a docker-machine VM, and installs docker client in the container (at runtime), so it can match the external.

##Running
In the directory above docker_jenkins, define a plugins.txt file that lists the plugins you want to be automatically installed in jenkins, e.g.

```
git
workflow-aggregator:2.2
cloudbees-credentials:3.3
tap:2.0.1
matrix-auth:1.5
mask-passwords:2.8
credentials-binding:1.13
credentials:2.1.17
xunit:1.102
```

Create a python 3.6+ virtualenv and activate it, then

```
pip install -e docker_jenkins_utils
```

Followed by

```
./up
```

to bring up the environment.

```
./down
```

will stop the environment.


##Running projects manually

If you just want to run a Jenkinsfile based project manually, create a python 3.6+ virtualenv and activate it, then

```
pip install -e docker_jenkins_utils
pip install -r run_project_requirements.txt
```

In the directory above docker_jenkins, define a plugins.txt file that lists the plugins you want to be automatically installed in jenkins, e.g.

```
git
workflow-aggregator:2.2
cloudbees-credentials:3.3
tap:2.0.1
matrix-auth:1.5
mask-passwords:2.8
credentials-binding:1.13
credentials:2.1.17
xunit:1.102
pipeline-model-definition
```

Then, to load a separate project directory into gitlab and create and run a project for it:

```
python run_project.py <directory_containing_jenkinsfile>
```

The directory_containing_jenkinsfile will be copied to a temporary directory, turned into a git project, and loaded into gitlab running in docker.  Then a job in jenkins will be created and run against that project.

You can set global environment variables in jenkins by placing them into a .env file:

```
FOO=BAR
```

The run_project.py script will automatically search from the current directory upward for a .env file, and load any variables it finds as jenkins global environment variables which can be accessed by your Jenkinsfile.

The Jenkins console is available on port 8080 wherever you docker daemon is running.  For example, if you are running a typical docker installation where containers are available at localhost, the http://localhost:8080 will take you to the jenkins console.  The default credentials are admin/admin.


##Caveats

- in experimental stage
- does not fully mimic DevOps production env; contains the minimum necessary to begin testing the jenkins-pipeline-docker.  Additional features will be added as needed.