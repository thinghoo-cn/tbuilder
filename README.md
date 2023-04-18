# Infras Builder

> 注意⚠️：本项目开源并遵从 MIT 协议。

Quick builder for images and version.
Check the [roadmap](./docs/roadmap.md) to know the new features.

## Install

```bash
# from nexus
pip install tbuilder

# install 1.*
pip install "tbuilder<2.0"

# install 2.*
pip install "tbuilder<3.0"
```


## USAGE

```bash
Usage: tbuilder [OPTIONS] COMMAND [ARGS]...

  tbuilder is an application to build image.

Options:
  --help  Show this message and exit.

Commands:
  build     build according to the config.yml
  check     check the git repository
  checkout  checkout current git repo version.
  clone     clone the repo in the repo list
  gen       generate config file
  http      start authed http server
  pull      pull the code in branch, and update the config.yml
  push      push current update to remote
  save      save the docker image
  show      show the current info
  update    update the version and hash from config.yml
  version   show tbuilder version
```

## Documentation

Read the [mkdocs](./docs/index.md)

## LICENSE

MIT
