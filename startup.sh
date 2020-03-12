#! /bin/bash
#Install nvm
sudo chown jenkins:jenkins /var/jenkins_home/workspace
rm -f /var/jenkins_home/.ssh/known_hosts # reset known hosts in case gitlab, etc location has changed
set -e
echo "installing plugins"
/usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt
echo "plugins installed"
echo "copying artifactory plugin configuration"
cp /tmp/artifactory_plugin.xml /var/jenkins_home/org.jfrog.hudson.ArtifactoryBuilder.xml
chown jenkins:jenkins /var/jenkins_home/org.jfrog.hudson.ArtifactoryBuilder.xml

/usr/local/bin/jenkins_orig.sh


