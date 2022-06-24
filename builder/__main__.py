import sys
import argparse
from .core.conf import STAGE_CONSTRAINT, logger, Config, get_current_repo
from .core.version import VersionHandler
from .core.hash_checker import HashChecker
from .core.images import build as image_build, save_image
from .core.httpserver import start_http


def cli():
    parser = argparse.ArgumentParser(description='tbuilder is an application to build image.')
    parser.add_argument('cmd', choices=['check', 'build', 'save', 'gen', 'show', 'http', 'version', 'update'],
                        help='select one command to run.')
    parser.add_argument('--username', type=str, help='http server username')
    parser.add_argument('--password', type=str, help='http server password')
    parser.add_argument('--port', type=int, help='http server port.')
    parser.add_argument('--stage', type=str, choices=['master', 'test', 'prd', 'demo', 'dev'],
                        help='stage information.')
    # parser.add_argument('--without-check', type=bool, help='build without check', default=False)

    args = parser.parse_args()

    if args.cmd == 'version':
        import pkg_resources
        builder = pkg_resources.require('builder')
        logger.info(f'tbuilder(builder) version is: {builder[0].version}')
    elif args.cmd == 'http':
        start_http(USERNAME=args.username, PASSWORD=args.password, port=args.port)
        sys.exit(0)
    else:
        CONFIG: Config = Config.load_config()
        current_repo = get_current_repo()

        checker = HashChecker(current_repo, config=CONFIG)
        v_h = VersionHandler(current_repo)
        if args.cmd == 'check':
            checker.check_hash()
            v_h.show_hash()
        elif args.cmd == 'build':
            checker.check_hash()
            v_h.show_hash()
            image_build(config=CONFIG)
        elif args.cmd == 'save':
            save_image(config=CONFIG)
        elif args.cmd == 'gen':
            CONFIG.gen()
        elif args.cmd == 'show':
            logger.info(CONFIG.repo_list)
        elif args.cmd == 'update':
            v_h.update_repos(args.stage)


if __name__ == '__main__':
    cli()