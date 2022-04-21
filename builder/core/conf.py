import os
import pathlib
import sys
from dataclasses import dataclass
from typing import Iterable, Tuple

import yaml
from dataclasses_json import dataclass_json
from loguru import logger
from git import Repo, InvalidGitRepositoryError

from .entity.all import RepoInstance, Version

if not os.getenv("DEBUG", False):
    logger.add('info.log')


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


def get_current_repo() -> Repo:
    try:
        current_repo = Repo('.')
        return current_repo
    except InvalidGitRepositoryError:
        logger.error('not a valid git repo.')
        sys.exit(1)


current_repo = get_current_repo()


@dataclass_json
@dataclass
class Config:
    key_file: str
    image_folder: str
    prefix: str
    version: str
    repo_list: Tuple[RepoInstance] = (
        RepoInstance(folder="./qms_backend", hash="test", image="app", key=True),
        RepoInstance(folder="./", hash="test", image="nginx", key=False),
    )

    def get_image_list(self) -> Iterable[str]:
        for r in self.repo_list:
            yield r.image

    @staticmethod
    def gen():
        path = './config.yml'
        logger.info(f'write to {path}')
        p = pathlib.Path(path)
        with p.open('w'):
            p.write_text(EXAMPLE_FILE)

    @classmethod
    def load_config(cls) -> 'Config':
        config_path = pathlib.Path('./config.yml')
        if not config_path.exists():
            logger.critical('config.yml not exist. generate!')
            cls.gen()
        with config_path.open() as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return Config.from_dict(data)

    def get_version(self) -> Version:
        return Version.parse_str(self.version)

    def get_prefix(self) -> str:
        """
        获取镜像的 prefix
        """
        if self.is_mes:
            prefix = "mes-compose"
        else:
            prefix = "qms-compose"
        return prefix

    def generate_image_version_path(self) -> pathlib.Path:
        """
        生成镜像+版本的路径
        """
        image_path = pathlib.Path(f"{self.image_folder}/{self.get_version().get_full('_')}")
        if not image_path.exists():
            image_path.mkdir()
        return image_path


CONFIG: Config = Config.load_config()