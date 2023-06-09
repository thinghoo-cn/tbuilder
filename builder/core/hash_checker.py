from git import Repo
from .conf import logger

from builder.core.conf import Config
from builder.core.entity.repo_instance import RepoInstance
from builder.core.error import BuilderError, HashInvalidError


class HashChecker:
    def __init__(self, repo: Repo, config: Config):
        self.repo = repo
        self.config = config

    @staticmethod
    def check_equal(sub_r, config: RepoInstance):
        # 检查 module hash 是否相等
        hash_ = sub_r.module().head.commit
        if str(hash_) != config.hash:
            raise HashInvalidError(f"submodule {sub_r.name}, {hash_} != {config.hash}")

    def check_hash(self):
        """ """
        for sub_r in self.repo.submodules:
            find = False
            for config_r in self.config.repo_list:
                if sub_r.name == config_r.name:
                    find = True
                    self.check_equal(sub_r, config_r)
            if not find:
                raise BuilderError(f"submodule {sub_r.name} not found.")
