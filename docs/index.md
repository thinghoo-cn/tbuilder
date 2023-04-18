# Thinghoo builder

Tbuilder means `thinghoo builder`.
Tbuilder is a tool to quick build images for deployment.

## Goal

1. Make build procecure easier.
2. Reduce error while building images.
3. Versionize the web application.

## Usage

```
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
