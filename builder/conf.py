from dataclasses import dataclass
from typing import List
from .entity.all import Version, Repo


version = Version(0, 1, 6)

RepoList: List[Repo] = [
    Repo(folder="./qms_backend", hash="test", image="app", key=True),
    Repo(folder="./", hash="test", image="nginx", key=False),
]

KEY_NAME = "~/.ssh/id_rsa"

IMAGE_FOLDER = "/root/services/images"


@dataclass
class Config:
    is_mes = False

    def get_prefix(self) -> str:
        if self.is_mes:
            prefix = "mes-compose"
        else:
            prefix = "qms-compose"
        return prefix


conf = Config()