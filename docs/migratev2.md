# Migrating from v1 to v2.

update config.yml.

1. version update.
2. repo_url update.

```yml
name: mes
+ version: 0.10.0.202304
image_folder: /root/services/images
prefix: mes-compose
cache: true
is_save_local: true
repo_list:
- + repo_url: git@gitee.com:beijing_epoch/e-mes-frontend.git
  code_folder: ./e-mes-frontend
  build_folder: ./
  hash: 2589d553e8595993bafd060e47bee58eace1493c
  image: nginx
  key: ssh
  key_file: ~/.ssh/id_rsa
  name: e-mes-frontend
- + repo_url: git@gitee.com:beijing_epoch/E-MES-backend.git
  code_folder: ./e-mes-backend
  build_folder: ./e-mes-backend
  hash: 3ee7c96a27ba1ef0e20fc96a58549f19e962f812
  image: app
  key: netrc
  key_file: ~/.netrc
  name: e-mes-backend

```