#!/usr/bin/env python3
from .conf import version, prefix
import pathlib
from typing import List
from invoke import Context
from loguru import logger



def save_image():
    c = Context()
    image_list: List[str] = ['app', 'nginx']
    image_list = [ f'{prefix}_{name}' for name in image_list ]

    image_path = pathlib.Path(f"/root/services/images/{version.get_full('_')}")
    if not image_path.exists():
        image_path.mkdir()

    with c.cd(str(image_path)):
        for image in image_list:
            current_version = f'{image}:{version.get_full(split=".")}'
            filename_version = f'{image}_{version.get_full(split="_")}.tgz'

            is_tag = False
            if is_tag:
            # make tag of latest image.
                tag_command = f'docker tag {image}:latest {current_version}'
                c.run(tag_command)
                logger.info(f'Image tagged: {tag_command}')

            save_command = (f'docker save {current_version} | gzip > {filename_version}')
            # run command
            c.run(save_command)
            logger.info(f'Image saved: {save_command}')


def main():
    save_image()


if __name__ == "__main__":
    main()
