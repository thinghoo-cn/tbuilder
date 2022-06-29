#!/usr/bin/env python
from git import Repo
from invoke import Context

from .conf import Config, logger, STAGE_CONSTRAINT
from .error import BuilderError, HashInvalidError

# repo is a Repo instance pointing to the git-python repository.
# For all you know, the first argument to Repo is a path to the repository
# you want to work with


class VersionHandler:
    def __init__(self, repo: Repo) -> None:
        self.repo = repo
        pass

    def show_hash(self):
        """
        展示子模块 hash
        """
        assert not self.repo.bare

        if not self.repo.submodules:
            logger.info("no submodules.")
        for r in self.repo.submodules:
            logger.info(r.name + ": " + str(r.module().head.commit))

    def select_version(self, config: Config):
        """
        调整子模块版本
        """
        for repo in config.repo_list:
            c = Context()
            with c.cd(repo.folder):
                c.run(f"git reset --hard {repo.hash}")

    def update_repos(self, stage: STAGE_CONSTRAINT):
        """按照分支，更新 compose 内部的代码"""
        assert stage, "stage must be exist."
        logger.info("update repos ...")
        from datetime import datetime

        c = Context()
        for r in self.repo.submodules:
            with c.cd(r.name):
                c.run("git reset --hard")
                logger.info(f"{r.name} pull from {stage}...")
                c.run(f"git pull origin {stage}")

        c.run("git pull")
        c.run("git add .")
        c.run(
            f'git commit --allow-empty -m "feat: update remote repository at {datetime.now().date()}"'
        )
        c.run("git push")
