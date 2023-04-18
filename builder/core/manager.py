#!/usr/bin/env python
import sys
import os
from git import Repo
from invoke import Context

from .conf import Config, logger

# repo is a Repo instance pointing to the git-python repository.
# For all you know, the first argument to Repo is a path to the repository
# you want to work with


class SourceCodeManager:
    def __init__(self, repo: Repo, config: Config) -> None:
        self.repo = repo
        self.config: Config = config

    def clone(self):
        c = Context()
        for r in self.config.repo_list:
            c.run(f'git clone {r.repo_url} {r.code_folder}')

    def show_hash(self):
        """
        展示子模块 hash
        """
        if self.repo.bare:
            raise Exception(f"repo {self.repo} is bare.")

        if not self.repo.submodules:
            logger.info("no submodules.")
        for r in self.repo.submodules:
            logger.info(r.name + ": " + str(r.module().head.commit))

    def select_version(self):
        """
        调整子模块版本
        """
        for repo in self.config.repo_list:
            c = Context()
            with c.cd(repo.code_folder):
                c.run(f"git reset --hard {repo.hash}")

    def update_repos(self, stage):
        """按照分支，更新 compose 内部的代码"""
        assert stage, "stage must be exist."
        logger.info("update repos ...")

        c = Context()
        for r in self.repo.submodules:
            if r.active_branch.name != stage:
                print(f'compose repo<{r.name}>: {r.active_branch.name} is not equal to {stage}.')
                sys.exit(-1)
            if os.path.exists(r.name):
                print(f'repo<{r.name}> is not exist.')
                sys.exit(-1)

            with c.cd(r.name):
                # remove files not in git.
                c.run('git clean -f -d')
                c.run("git reset --hard")
                logger.info(f"{r.name} pull from {stage}...")

                # stage is branch.
                c.run(f"git pull origin {stage}")

        # 获取 commit hash，写入 config.yml
        for r in self.config.repo_list:
            if not os.path.exists(r.code_folder):
                print(f'repo <{r.code_folder}> is not exist')
                sys.exit(-1)

            repo = Repo(r.code_folder)
            r.hash = str(repo.commit())
        self.config.write_back()
        self.push_repo()

    def push_repo(self):
        """将当前 compose 更新到远程"""
        from datetime import datetime
        c = Context()
        c.run("git pull")
        c.run("git add .")
        c.run(f'git commit --allow-empty -m "feat: update remote repository at {datetime.now().date()}"')
        c.run("git push")
