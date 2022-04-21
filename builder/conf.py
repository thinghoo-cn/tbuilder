import os
from dataclasses import dataclass
from typing import List
from loguru import logger
from .entity.all import Version, RepoInstance


if not os.getenv("DEBUG", False):
    logger.add('info.log')


repo_list: List[RepoInstance] = [
    RepoInstance(folder="./qms_backend", hash="test", image="app", key=True),
    RepoInstance(folder="./", hash="test", image="nginx", key=False),
]


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


conf = Config()
