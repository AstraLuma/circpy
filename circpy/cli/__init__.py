from ._top import parser
from . import pull, push, wifi  # noqa


def main():
    args = parser.parse_args()
    args.func(args)
