from __future__ import print_function
import click
from command_jenkins import jenkins
from command_git import git
import jenkins_common
from docker_jenkins_utils.common import getGitServer


@click.group()
def cli():
    pass


@click.command()
def clean():
    getGitServer.deleteRepos()
    jenkins_common.clearEnvVars()


cli.add_command(jenkins)
cli.add_command(git)
cli.add_command(clean)

if __name__ == '__main__':
    cli()
