from typing import List
from .entity.all import Version, Repo


version = Version(0, 1, 6)

is_mes = False
if is_mes:
    prefix = "mes-compose"
else:
    prefix = "qms-compose"


RepoList: List[Repo] = [
    Repo(folder='./qms_backend', hash='test', image='app', key=True),
    Repo(folder='./', hash='test', image='nginx', key=False),
]

KEY_NAME = "~/.ssh/id_rsa"