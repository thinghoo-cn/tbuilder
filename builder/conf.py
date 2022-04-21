import os
import pathlib
from dataclasses import dataclass
from typing import Iterable, Tuple

from loguru import logger

from .entity.all import RepoInstance, Version

if not os.getenv("DEBUG", False):
    logger.add('info.log')


@dataclass
class RepoManager:
    repo_list: Tuple[RepoInstance] = (
        RepoInstance(folder="./qms_backend", hash="test", image="app", key=True),
        RepoInstance(folder="./", hash="test", image="nginx", key=False),
    )

    def get_image_list(self) -> Iterable[str]:
        for r in self.repo_list:
            yield r.image


@dataclass
class Config:
    KEY_NAME: str = "~/.ssh/id_rsa"
    IMAGE_FOLDER: str = "/root/services/images"
    is_mes = False
    version = Version(0, 1, 6)

    def get_prefix(self) -> str:
        if self.is_mes:
            prefix = "mes-compose"
        else:
            prefix = "qms-compose"
        return prefix

    def generate_image_version_path(self) -> pathlib.Path:
        image_path = pathlib.Path(f"{self.IMAGE_FOLDER}/{self.version.get_full('_')}")
        if not image_path.exists():
            image_path.mkdir()
        return image_path


conf = Config()
repo_manager = RepoManager()
