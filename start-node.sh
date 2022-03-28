#!/bin/bash
sudo service ssh restart
java -jar /home/jenkins/agent.jar -jnlpUrl "http://jenkins:8080/computer/ec2-worker-u20-graviton/jenkins-agent.jnlp" -workDir /home/jenkins/workspace -failIfWorkDirIsMissing