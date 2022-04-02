import pathlib
from git.repo import Repo


def clone(url, path: pathlib.Path) -> Repo:
    r = Repo.clone_from(url, path)
    return r
