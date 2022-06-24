# Thinghoo builder

Tbuilder means `thinghoo builder`.
Tbuilder is a tool to quick build images for deployment.

## Goal

1. Make build procecure easier.
2. Reduce error while building images.
3. Versionize the web application.

## Usage

```
usage: tbuilder [-h] [--username USERNAME] [--password PASSWORD] [--port PORT] [--stage {master,test,prd,demo,dev}]
                {check,build,save,gen,show,http,version,update}

tbuilder is an application to build image.

positional arguments:
  {check,build,save,gen,show,http,version,update}
                        select one command to run.

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME   http server username
  --password PASSWORD   http server password
  --port PORT           http server port.
  --stage {master,test,prd,demo,dev}
                        stage information.

```
