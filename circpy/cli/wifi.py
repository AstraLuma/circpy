from . import _top


def wifi(args):
    raise NotImplementedError


parser = _top.subparsers.add_parser('wifi', help='Configure WiFi credentials')
parser.set_defaults(func=wifi)
