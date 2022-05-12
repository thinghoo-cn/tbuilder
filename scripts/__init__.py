from dataclasses import dataclass
from typing import List
from fabric import Connection


@dataclass
class Runner:
    version: str
    server_list: List[Connection]

    def update(self):
        for s in self.server_list:
            s.put(f'dist/builder-{self.version}-py3-none-any.whl')
            s.run(f'pip install -r {self.version}')
