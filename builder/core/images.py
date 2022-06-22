from builder.core.entity.repo_instance import RepoInstance
from .conf import logger, Config, image_registry, is_tag, is_save_local
from invoke import Context


def generate_cmd(config: Config, r: RepoInstance) -> str:
    full_image_name = f"{config.get_prefix()}_{r.image}"

    if r.key == 'netrc':
        key_param = f'--build-arg netrc="$(cat {config.key_file})"'
    elif r.key == 'ssh':
        key_param = f'--build-arg ssh_prv_key="$(cat {config.key_file})"'
    else:
        key_param = ''

    cache_opt = '' if config.cache else '--no-cache'
    full_cmd = f"docker build {cache_opt} {key_param}"
    if r.key:
        full_cmd = f"{full_cmd} -t {full_image_name}:{config.get_version().get_full()} ."
    else:
        full_cmd = (
            f"{full_cmd} -t {full_image_name}:{config.get_version().get_full()} ."
        )
    return full_cmd


def build(config: Config):
    """
    构建镜像
    """
    for r in config.repo_list:
        c = Context()
        with c.cd(r.folder):
            full_cmd = generate_cmd(config=config, r=r)
            logger.info("run: " + full_cmd)
            c.run(full_cmd)


def save_image(config: Config):
    """
    保存镜像
    """
    c = Context()
    image_list = config.get_image_list()
    image_list = [f"{config.get_prefix()}_{name}" for name in image_list]

    # 生成镜像版本路径
    image_path = config.generate_image_version_path()

    with c.cd(str(image_path)):
        for image in image_list:
            current_version = f'{image}:{config.get_version().get_full(split=".")}'
            filename_version = f'{image}_{config.get_version().get_full(split="_")}.tgz'

            if is_tag:
                # make tag of latest image.
                tagged_name = f"{image_registry}/{config.name}/{current_version}"
                tag_command = f"docker tag {current_version} {tagged_name}"
                c.run(tag_command)
                c.run(f'docker push {tagged_name}')
                logger.info(f"Image pushed: {tag_command}")

            if is_save_local:
                save_command = f"docker save {current_version} | gzip > {filename_version}"
                # run command
                c.run(save_command)
                logger.info(f"Image saved: {save_command}")
