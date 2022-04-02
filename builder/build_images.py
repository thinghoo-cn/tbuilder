from .conf import conf, RepoList, version as v, KEY_NAME
from invoke import Context
from loguru import logger


def build():
    for r in RepoList:
        c = Context()
        with c.cd(r.folder):
            full_image_name = f"{conf.get_prefix()}_{r.image}"
            key_param = f'--build-arg ssh_prv_key="$(cat {KEY_NAME})"'
            if r.key:
                full_cmd = f"docker build --no-cache {key_param} -t {full_image_name}:{v.get_full()} ."
            else:
                full_cmd = (
                    f"docker build --no-cache -t {full_image_name}:{v.get_full()} ."
                )
            logger.info("run: " + full_cmd)
            c.run(full_cmd)
