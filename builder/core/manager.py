#!/usr/bin/env python
import sys
import os
from git import Repo
from invoke import Context

from builder.core.entity.repo_instance import RepoInstance

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

    def pull_from_remote(self, c: Context, r: Repo, stage: str):
        """
        git pull code from remote repository, with branch {stage}.
        """
        with c.cd(r.name):
            # remove files not in git.
            c.run('git clean -f -d')
            c.run("git reset --hard")

            # check remote branch
            if not stage in r.remote().refs:
                print(f'ERROR: {stage} is not exist in {r.remote()}')
                sys.exit(-1)
            logger.info(f"{r.name} pull from {stage}...")
            # stage is branch.
            c.run(f"git pull origin {stage}")

    def check_stage(self, r: Repo, stage: str):
        """ check the git repository branch ~?= stage"""
        if r.active_branch.name != stage:
            # r has no name
            err_msg = f'ERROR: compose repo<{r.name}>: {r.active_branch.name} is not equal to {stage}.'
            print(err_msg, file=sys.stderr)
            sys.exit(-1)

    def check_folder(self, repo: RepoInstance):
        """ check the code_folder of repo exist or not"""
        if not os.path.exists(repo.code_folder):
            err_msg = f'ERROR: repo<{repo.name}> is not exist.'
            print(err_msg, file=sys.stderr)
            sys.exit(-1)

    def update_repos(self, stage):
        """按照分支，更新 compose 内部的代码"""
        assert stage, "stage must be exist."
        logger.info("update repos ...")

        c = Context()
        for repo in self.config.repo_list:
            self.check_folder(repo)
            r = Repo(repo.code_folder)
            r.name = repo.name
            self.check_stage(r, stage)
            self.pull_from_remote(c, r, stage)

        # 获取 commit hash，写入 config.yml
        for r in self.config.repo_list:
            if not os.path.exists(r.code_folder):
                print(f'ERROR: repo <{r.code_folder}> is not exist')
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
