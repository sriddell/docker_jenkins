import jenkins.model.*
import hudson.security.*
import hudson.security.Permission


def env = System.getenv()

def jenkins = Jenkins.getInstance()
jenkins.setSecurityRealm(new HudsonPrivateSecurityRealm(false))
jenkins.setAuthorizationStrategy(new GlobalMatrixAuthorizationStrategy())

def user = jenkins.getSecurityRealm().createAccount(env.JENKINS_USER, env.JENKINS_PASS)
user.save()

jenkins.getAuthorizationStrategy().add(Jenkins.ADMINISTER, env.JENKINS_USER)
Permission.getAll().each() {
    println("Adding " + it + " to " + env.JENKINS_USER)
    jenkins.getAuthorizationStrategy().add(it, env.JENKINS_USER)
}
jenkins.save()
