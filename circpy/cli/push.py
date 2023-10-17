from . import _top


def push(args):
    raise NotImplementedError


parser = _top.subparsers.add_parser('push', help='Push files to the board')
parser.set_defaults(func=push)
