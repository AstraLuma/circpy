import pathlib

from . import _top
from .. import _pathlib
from .. import junk_drawer


def pull(args):
    junk_drawer.walking_copy(args.board, args.dest)


parser = _top.subparsers.add_parser(
    'pull', help='Pull files from the board',
    parents=[_top.board_parser],
)
parser.add_argument('dest', help='Place to write files to', type=_pathlib.Path)
parser.set_defaults(func=pull)
