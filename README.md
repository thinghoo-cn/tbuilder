# Infras Builder

> 注意⚠️：本项目开源并遵从 MIT 协议。

Quick builder for images and version.
Check the [roadmap](./docs/roadmap.md) to know the new features.

## Install

`pip install -e .`

## RUN

```bash
Usage: tbuilder [OPTIONS] COMMAND [ARGS]...

  tbuilder is an application to build image.

Options:
  --help  Show this message and exit.

Commands:
  build     build according to the config.yml
  check     check the git repository
  checkout  checkout current git repo version.
  gen       generate config file
  http      start authed http server
  pull      pull the code in branch
  save      save the docker image
  show      show the current info
  update    升级 config.yml 中的版本
  version   show tbuilder version
```

## Documentation

Read the [mkdocs](./docs/index.md)

## LICENSE

MIT
