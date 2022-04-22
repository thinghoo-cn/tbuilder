#!/usr/bin/env python
from invoke import Context
from .conf import logger, CONFIG
from git import Repo
from .error import HashInvalidError, BuilderError

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
        logger.info(r.name + ': ' + str(r.module().head.commit))


def check_hash(repo: Repo):
    for sub_r in repo.submodules:
        find = False
        for config_r in CONFIG.repo_list:
            if sub_r.name == config_r.folder:
                find = True
                if sub_r.module().head.commit != config_r.hash:
                    raise HashInvalidError(f'f{sub_r.module().head.commit} != {config_r.hash}')
        if not find:
            raise BuilderError(f'submodule {sub_r.name} not found.')


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
