#!/usr/bin/env python
from invoke import Context
from .conf import RepoList, logger
from git import Repo

# repo is a Repo instance pointing to the git-python repository.
# For all you know, the first argument to Repo is a path to the repository
# you want to work with


def show_version(repo: Repo):
    assert not repo.bare

    for r in repo.submodules:
        logger.info(r.name, ':', r.module().head.commit)


def select_version():
    for repo in RepoList:
        c = Context()
        with c.cd(repo.folder):
            c.run(f"git reset --hard {repo.hash}")


if __name__ == "__main__":
    select_version()
