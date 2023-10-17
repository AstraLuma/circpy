import argparse

from .. import vfs

parser = argparse.ArgumentParser(
)

subparsers = parser.add_subparsers()

parser.set_defaults(func=lambda args: parser.print_help())

board_parser = argparse.ArgumentParser(add_help=False)
board_parser.add_argument(
    '--board', help='Board to use', type=vfs.from_url,
    # FIXME: Default from envvar
)
