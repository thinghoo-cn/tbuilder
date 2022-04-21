#!/usr/bin/env python
from invoke import Context
from .conf import logger, CONFIG
from git import Repo

# repo is a Repo instance pointing to the git-python repository.
# For all you know, the first argument to Repo is a path to the repository
# you want to work with


def show_hash(repo: Repo):
    """
    展示子模块 hash
    """
    assert not repo.bare

    if not repo.submodules:
        logger.info('no submodules.')
    for r in repo.submodules:
        logger.info(r.name + ':' + r.module().head.commit)


def select_version():
    """
    调整子模块版本
    """
    for repo in CONFIG.repo_list:
        c = Context()
        with c.cd(repo.folder):
            c.run(f"git reset --hard {repo.hash}")


if __name__ == "__main__":
    select_version()
