#! /bin/bash
#Install nvm
curl https://raw.githubusercontent.com/creationix/nvm/v0.25.3/install.sh | bash
set -e
echo "installing plugins"
/usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt
echo "plugins installed"
/usr/local/bin/jenkins_orig.sh


