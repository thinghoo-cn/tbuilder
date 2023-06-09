from dataclasses import dataclass
from typing import Literal


@dataclass
class RepoInstance:
    repo_url: str
    code_folder: str
    build_folder: str
    hash: str
    image: str
    key: Literal["ssh", "netrc", ""]
    key_file: str
    name: str = ""
