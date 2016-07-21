from __future__ import print_function
import click
from command_jenkins import jenkins
from command_git import git
import gitlab_common
import jenkins_common

@click.group()
def cli():
    pass

@click.command()
def clean():
    gitlab_common.deleteRepos()
    jenkins_common.clearEnvVars()

cli.add_command(jenkins)
cli.add_command(git)
cli.add_command(clean)

if __name__ == '__main__':
    cli()
