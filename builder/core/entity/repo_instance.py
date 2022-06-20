from dataclasses import dataclass
from typing import Literal


@dataclass
class RepoInstance:
    folder: str
    hash: str
    image: str
    key: Literal['ssh', 'netrc', '']
    name: str = ""
