import pathlib

from . import _top
from .. import _pathlib
from .. import junk_drawer


def push(args):
    junk_drawer.walking_copy(args.src, args.board)


parser = _top.subparsers.add_parser(
    'push', help='Push files to the board',
    parents=[_top.board_parser],
)
parser.add_argument('src', help='Place to read files from', type=_pathlib.Path)
parser.set_defaults(func=push)
