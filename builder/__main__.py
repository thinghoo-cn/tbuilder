import click
from .core.conf import current_repo, logger, CONFIG
from .core.version import show_hash
from .core.hash_checker import HashChecker
from .core.images import build as image_build, save_image


@click.command()
@click.argument('cmd', type=str, default='check')
def cli(cmd):
    checker = HashChecker(current_repo)
    checker.check_hash()
    if cmd == 'check':
        show_hash(current_repo)
    elif cmd == 'build':
        image_build()
    elif cmd == 'save':
        save_image()
    elif cmd == 'gen':
        CONFIG.gen()
    elif cmd == 'show':
        logger.info(CONFIG.repo_list)


if __name__ == '__main__':
    cli()
