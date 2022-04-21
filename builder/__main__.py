import pathlib

import click
from .core.conf import get_current_repo, logger
from .core.version import show_hash
from .core.images import build as image_build, save_image

EXAMPLE_FILE = """
name: qms_backend
version: 0.1.0
key_file: ~/.ssh/id_rsa
image_folder: /root/services/images
prefix: qms-compose

repo_list:
  - name: backend
    folder: ./qms_backend
    hash: test
    image: app
    key: true
  - name: frontend
    folder: ./
    hash: test
    image: nginx
    key: true
"""


@click.command()
@click.argument('cmd', type=str, default='check')
def cli(cmd):
    if cmd == 'check':
        show_hash(get_current_repo())
    elif cmd == 'build':
        image_build()
    elif cmd == 'save':
        save_image()
    elif cmd == 'gen':
        path = './config.yml'
        logger.info(f'write to {path}')
        p = pathlib.Path(path)
        with p.open('w'):
            p.write_text(EXAMPLE_FILE)


if __name__ == '__main__':
    cli()
