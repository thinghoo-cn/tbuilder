from .conf import logger, Config
from invoke import Context


def build(config: Config):
    """
    构建镜像
    """
    for r in config.repo_list:
        c = Context()
        with c.cd(r.folder):
            full_image_name = f"{config.get_prefix()}_{r.image}"
            key_param = f'--build-arg ssh_prv_key="$(cat {config.key_file})"'
            cache_opt = '' if config.cache else '--no-cache'
            if r.key:
                full_cmd = f"docker build {cache_opt} {key_param} -t {full_image_name}:{config.get_version().get_full()} ."
            else:
                full_cmd = (
                    f"docker build {cache_opt} -t {full_image_name}:{config.get_version().get_full()} ."
                )
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

            is_tag = False
            if is_tag:
                # make tag of latest image.
                tag_command = f"docker tag {image}:latest {current_version}"
                c.run(tag_command)
                logger.info(f"Image tagged: {tag_command}")

            save_command = f"docker save {current_version} | gzip > {filename_version}"
            # run command
            c.run(save_command)
            logger.info(f"Image saved: {save_command}")
