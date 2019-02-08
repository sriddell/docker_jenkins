#! /bin/bash
#Install nvm
sudo chown jenkins:jenkins /var/jenkins_home/workspace
set -e
echo "installing plugins"
/usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt
echo "plugins installed"
echo "copying artifactory plugin configuration"
cp /tmp/artifactory_plugin.xml /var/jenkins_home/org.jfrog.hudson.ArtifactoryBuilder.xml
chown jenkins:jenkins /var/jenkins_home/org.jfrog.hudson.ArtifactoryBuilder.xml

/usr/local/bin/jenkins_orig.sh


