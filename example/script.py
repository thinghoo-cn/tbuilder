# check the script.
import os
import shutil

cmd = 'git clone git@gitee.com:beijing_epoch/mes-compose.git'
# change directory.
if os.path.exists('./example'):
    os.chdir('./example')
os.system(cmd)

# input your config.yml
if os.path.exists('./mes-compose'):
    shutil.copy('./config.example.yml', './mes-compose/config.yml')
else:
    raise Exception('no valid path')

# load sub module
cmd = 'git submodule update --init'
if os.path.exists('./mes-compose'):
    os.chdir('./mes-compose')
os.system(cmd)