from invoke import Context
from .conf import RepoList



def select_version():
    for repo in RepoList:
        c = Context()
        with c.cd(repo.folder):
            c.run(f'git reset --hard {repo.hash}')


if __name__ == "__main__":
    select_version()
