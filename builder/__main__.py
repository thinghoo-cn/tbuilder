import argparse
from .core.conf import current_repo, logger, CONFIG
from .core.version import show_hash
from .core.hash_checker import HashChecker
from .core.images import build as image_build, save_image


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tbuilder is an application to build image.')
    parser.add_argument('cmd', choices=['check', 'build', 'save', 'gen', 'show'],
                        help='select one command to run.')
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
