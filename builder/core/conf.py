import os
import pathlib
import sys
from dataclasses import dataclass, asdict
from typing import Iterable, OrderedDict, Tuple, List, Literal

import yaml
from dataclasses_json import dataclass_json
from loguru import logger
from git import Repo, InvalidGitRepositoryError

from .entity.all import RepoInstance, Version

if not os.getenv("DEBUG", False):
    logger.add("info.log")


EXAMPLE_FILE = """
name: qms_backend
version: 0.1.0
image_folder: /root/services/images
prefix: qms-compose

repo_list:
  - name: backend
    build_folder: ./qms_backend
    code_folder: ./qms_backend
    hash: test
    key_file: ~/.ssh/id_rsa
    image: app
    key: true
  - name: frontend
    build_folder: ./
    code_builder: ./qms_frontend
    key_file: ~/.ssh/id_rsa
    hash: test
    image: nginx
    key: true
"""

STAGE_CONSTRAINT = Literal["master", "test", "prd", "demo", "dev"]


def get_current_repo() -> Repo:
    try:
        current_repo = Repo(".")
        return current_repo
    except InvalidGitRepositoryError:
        logger.error("not a valid git repo.")
        sys.exit(1)


@dataclass_json
@dataclass
class Config:
    name: str
    image_folder: str
    prefix: str
    version: str

    # is pushed to registry
    is_tag: bool = True
    is_save_local: bool = False
    cache: bool = False

    repo_list: Tuple[RepoInstance, RepoInstance] = (
        RepoInstance(build_folder="./qms_backend", code_folder="", hash="test", image="app", key="ssh", key_file='~/.netrc'),
        RepoInstance(build_folder="./", code_folder="", hash="test", image="nginx", key="ssh", key_file='~/.netrc'),
    )

    def get_image_list(self) -> Iterable[str]:
        for r in self.repo_list:
            yield r.image

    @staticmethod
    def gen():
        path = "./config.yml"
        logger.info(f"write to {path}")
        p = pathlib.Path(path)
        with p.open("w"):
            p.write_text(EXAMPLE_FILE)

    @classmethod
    def load_config(cls) -> "Config":
        config_path = pathlib.Path("./config.yml")
        if not config_path.exists():
            logger.critical("config.yml not exist!")
            sys.exit(-1)
        with config_path.open() as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return Config.from_dict(data)

    def get_version(self) -> Version:
        return Version.parse_str(self.version)

    def get_prefix(self) -> str:
        """
        获取镜像的 prefix
        """
        return self.prefix

    def generate_image_version_path(self) -> pathlib.Path:
        """
        生成镜像+版本的路径
        """
        image_path = pathlib.Path(
            f"{self.image_folder}/{self.get_version().get_full('_')}"
        )
        if not image_path.exists():
            image_path.mkdir()
        return image_path

    def to_ordered_dict(self):
        od = {}
        od['name'] = self.name
        od['version']= self.version
        od['image_folder'] = self.image_folder
        od['prefix'] = self.prefix
        od['cache'] = self.cache
        od['is_save_local'] = self.is_save_local
        od['repo_list'] = [asdict(x) for x in self.repo_list]
        return od

    def write_back(self):
        """将变化写回 config.yml"""
        # data = self.to_ordered_dict()
        data = self.to_ordered_dict()
        with open('./config.yml', 'w') as f:
            yaml.dump(data, f, sort_keys=False, default_flow_style=False)


image_registry = "harbor.beijing-epoch.com"
