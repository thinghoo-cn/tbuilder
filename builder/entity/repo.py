from dataclasses import dataclass


@dataclass
class Repo:
    folder: str
    hash: str
    image: str
    key: bool
