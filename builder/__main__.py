import argparse
from ast import arg
from tracemalloc import start
from xml.etree.ElementInclude import default_loader
from .core.conf import current_repo, logger, CONFIG
from .core.version import show_hash
from .core.hash_checker import HashChecker
from .core.images import build as image_build, save_image
from .core.httpserver import start_http


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tbuilder is an application to build image.')
    parser.add_argument('cmd', choices=['check', 'build', 'save', 'gen', 'show', 'http'],
                        help='select one command to run.')
    parser.add_argument('--username', type=str, help='http server username')
    parser.add_argument('--password', type=str, help='http server password')
    parser.add_argument('--port', type=int, help='http server port.')

    args = parser.parse_args()

    checker = HashChecker(current_repo)
    checker.check_hash()
    if args.cmd == 'check':
        show_hash(current_repo)
    elif args.cmd == 'build':
        image_build()
    elif args.cmd == 'save':
        save_image()
    elif args.cmd == 'gen':
        CONFIG.gen()
    elif args.cmd == 'show':
        logger.info(CONFIG.repo_list)
    elif args.cmd == 'http':
        start_http(USERNAME=args.username, PASSWORD=args.password, port=args.port)

