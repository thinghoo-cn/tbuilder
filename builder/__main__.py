import sys

import click

from .core.conf import Config, get_current_repo, logger
from .core.hash_checker import HashChecker
from .core.httpserver import start_http
from .core.images import ImageManager
from .core.version import VersionHandler


@click.group(help="tbuilder is an application to build image.")
def cli():
    pass


@click.command(help="check the git repository")
def check():
    CONFIG: Config = Config.load_config()
    current_repo = get_current_repo()

    checker = HashChecker(current_repo, config=CONFIG)
    v_h = VersionHandler(current_repo)

    checker.check_hash()
    v_h.show_hash()


@click.command(help="build according to the config.yml")
def build():
    CONFIG: Config = Config.load_config()
    current_repo = get_current_repo()

    checker = HashChecker(current_repo, config=CONFIG)
    v_h = VersionHandler(current_repo)
    i_m = ImageManager(config=CONFIG)

    checker.check_hash()
    v_h.show_hash()
    i_m.build()


@click.command(help="save the docker image")
def save():
    CONFIG: Config = Config.load_config()
    i_m = ImageManager(config=CONFIG)
    i_m.save()


@click.command(help="generate config file")
def gen():
    CONFIG: Config = Config.load_config()
    CONFIG.gen()


@click.command(help="checkout current git repo version.")
@click.option("--stage", type=str, help="the stage of current compose")
def checkout(stage):
    CONFIG: Config = Config.load_config()
    current_repo = get_current_repo()
    v_h = VersionHandler(current_repo)

    v_h.update_repos(stage)
    v_h.select_version(CONFIG)


@click.command(help="show the current info")
def show():
    CONFIG: Config = Config.load_config()
    for repo in CONFIG.repo_list:
        logger.info(repo)


@click.command(help="pull the code in branch, and update the config.yml")
@click.option("--stage", type=str, help="the stage of current compose")
def pull(stage):
    CONFIG: Config = Config.load_config()
    current_repo = get_current_repo()
    v_h = VersionHandler(current_repo, CONFIG)
    v_h.update_repos(stage)


@click.command(help="start authed http server")
@click.option("--username", type=str, help="http server username")
@click.option("--password", type=str, help="http server password")
@click.option("--port", type=int, help="http server port")
def http(username, password, port):
    start_http(USERNAME=username, PASSWORD=password, port=port)
    sys.exit(0)


@click.command(help="show tbuilder version")
def version():
    import pkg_resources

    builder = pkg_resources.require("builder")
    print(f"tbuilder(builder) version is: {builder[0].version}")


@click.command(help="update the version and hash from config.yml")
@click.option("--stage", type=str, help="the stage of current compose")
def update(stage):
    current_repo = get_current_repo()
    v_h = VersionHandler(current_repo)
    v_h.update_repos(stage)


@click.command(help="根据 config.yml 中的包下载")
def download():
    pass


cli.add_command(check)
cli.add_command(build)
cli.add_command(save)
cli.add_command(gen)
cli.add_command(checkout)
cli.add_command(show)
cli.add_command(pull)
cli.add_command(http)
cli.add_command(version)
cli.add_command(update)


if __name__ == "__main__":
    cli()
