#!/bin/bash
sudo service ssh restart
sudo start-docker.sh
java -jar /home/jenkins/agent.jar -jnlpUrl "http://jenkins:8080/computer/$WORKER_NAME/jenkins-agent.jnlp" -workDir /home/jenkins/workspace -failIfWorkDirIsMissing