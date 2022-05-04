#! /bin/bash
#Install nvm
sudo chown jenkins:jenkins /var/jenkins_home/workspace
rm -f /var/jenkins_home/.ssh/known_hosts # reset known hosts in case gitea, etc location has changed
set -e
echo "installing plugins"
cp /usr/share/jenkins/ref/plugins.txt /var/jenkins_home/plugins.txt
/usr/local/bin/install-plugins.sh < /var/jenkins_home/plugins.txt
rm /var/jenkins_home/plugins.txt
#echo "configuration-as-code" >> /usr/local/bin/install-plugins.sh
echo "plugins installed"
echo "copying artifactory plugin configuration"
cp /tmp/artifactory_plugin.xml /var/jenkins_home/org.jfrog.hudson.ArtifactoryBuilder.xml
chown jenkins:jenkins /var/jenkins_home/org.jfrog.hudson.ArtifactoryBuilder.xml

mkdir -p /var/jenkins_home/.ssh
ssh-keyscan -H gitea >> /var/jenkins_home/.ssh/known_hosts
sudo chown jenkins:jenkins /var/jenkins_home/.ssh
sudo chown jenkins:jenkins /var/run/docker.sock

/usr/local/bin/jenkins_orig.sh


