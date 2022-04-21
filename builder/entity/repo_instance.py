from dataclasses import dataclass


@dataclass
class RepoInstance:
    folder: str
    hash: str
    image: str
    key: bool
