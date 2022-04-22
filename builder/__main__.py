import pathlib

import click
from .core.conf import current_repo, logger, CONFIG
from .core.version import show_hash, check_hash
from .core.images import build as image_build, save_image


@click.command()
@click.argument('cmd', type=str, default='check')
def cli(cmd):
    if cmd == 'check':
        show_hash(current_repo)
        check_hash(current_repo)
    elif cmd == 'build':
        image_build()
    elif cmd == 'save':
        save_image()
    elif cmd == 'gen':
        CONFIG.gen()


if __name__ == '__main__':
    cli()
