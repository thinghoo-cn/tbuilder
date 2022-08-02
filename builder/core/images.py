from builder.core.entity.repo_instance import RepoInstance
from .conf import logger, Config, image_registry
from invoke import Context


class ImageManager:
    def __init__(self, config: Config) -> None:
        self.config = config

    def _gen_cmd(self, r: RepoInstance) -> str:
        """生成镜像构建命令

        Args:
            r (RepoInstance): _description_

        Returns:
            str: 构建命令
        """
        full_image_name = f"{self.config.get_prefix()}_{r.image}"

        # set netrc and ssh key for image authentation.
        if r.key == "netrc":
            key_param = f'--build-arg netrc="$(cat {r.key_file})"'
        elif r.key == "ssh":
            key_param = f'--build-arg ssh_prv_key="$(cat {r.key_file})"'
        else:
            key_param = ""

        cache_opt = "" if self.config.cache else "--no-cache"
        full_cmd = f"docker build {cache_opt} {key_param}"
        if r.key:
            full_cmd = f"{full_cmd} -t {full_image_name}:{self.config.get_version().get_full()} ."
        else:
            full_cmd = f"{full_cmd} -t {full_image_name}:{self.config.get_version().get_full()} ."
        return full_cmd

    def build(self):
        """
        构建镜像
        """
        for r in self.config.repo_list:
            c = Context()
            with c.cd(r.build_folder):
                full_cmd = self._gen_cmd(r=r)
                logger.info("run: " + full_cmd)
                c.run(full_cmd)

    def save(self):
        """
        保存镜像
        """
        c = Context()
        image_list = self.config.get_image_list()
        image_list = [f"{self.config.get_prefix()}_{name}" for name in image_list]

        # 生成镜像版本路径
        image_path = self.config.generate_image_version_path()

        with c.cd(str(image_path)):
            for image in image_list:
                current_version = (
                    f'{image}:{self.config.get_version().get_full(split=".")}'
                )
                filename_version = (
                    f'{image}_{self.config.get_version().get_full(split="_")}.tgz'
                )

                if self.config.is_tag:
                    # make tag of latest image.
                    tagged_name = (
                        f"{image_registry}/{self.config.name}/{current_version}"
                    )
                    tag_command = f"docker tag {current_version} {tagged_name}"
                    c.run(tag_command)
                    c.run(f"docker push {tagged_name}")
                    logger.info(f"Image pushed: {tag_command}")

                if self.config.is_save_local:
                    save_command = (
                        f"docker save {current_version} | gzip > {filename_version}"
                    )
                    # run command
                    c.run(save_command)
                    logger.info(f"Image saved: {save_command}")
