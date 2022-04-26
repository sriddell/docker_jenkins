#!/bin/bash
sudo service ssh restart
java -jar /home/jenkins/agent.jar -jnlpUrl "http://jenkins:8080/computer/$WORKER_NAME/jenkins-agent.jnlp" -workDir /home/jenkins/workspace -failIfWorkDirIsMissing