import os
import pathlib
from dataclasses import dataclass
from typing import Iterable, Tuple

import yaml
from dataclasses_json import dataclass_json
from loguru import logger

from .entity.all import RepoInstance, Version

if not os.getenv("DEBUG", False):
    logger.add('info.log')


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

    @classmethod
    def load_config(cls) -> 'Config':
        config_path = pathlib.Path('./config.yml')
        assert config_path, 'must have config.yml'
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
