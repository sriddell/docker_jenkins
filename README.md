#Experimental jenkins image for testing pipelines-as-code

##Overview

Builds jenkins into a container along with the workflow-aggregator plugin (for pipelines as code).  Based on the build for the official Jenkins docker image (https://github.com/jenkinsci/docker).

Also sets the docker group ID to match that in a docker-machine VM, and installs docker client in the container (at runtime), so it can match the external.

##Running

Testing a docker-build pipeline will require ECR access.  If you have used the sts tool to set temp aws credentials in your shell, the following should run the container (assuming you have built it and tagged it as jenkins) and allow access to the docker instance running it:

```
docker run -d --name jenkins -v /var/run/docker.sock:/var/run/docker.sock -p 8080:8080 -p 50000:50000 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION jenkins
```

##Caveats

- in experimental stage
- does not fully mimic DevOps production env; contains the minimum necessary to begin testing the jenkins-pipeline-docker.  Additional features will be added as needed.