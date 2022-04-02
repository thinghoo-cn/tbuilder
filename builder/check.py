#!/usr/bin/env python
from git import Repo

# rorepo is a Repo instance pointing to the git-python repository.
# For all you know, the first argument to Repo is a path to the repository
# you want to work with

def main():
    repo = Repo(".")
    assert not repo.bare

    for r in repo.submodules:
        print(r.name, ':', r.module().head.commit)


if __name__ == '__main__':
    main()