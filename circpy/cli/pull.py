from . import _top


def pull(args):
    raise NotImplementedError


parser = _top.subparsers.add_parser('pull', help='Pull files from the board')
parser.set_defaults(func=pull)
