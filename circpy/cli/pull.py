import pathlib

from . import _top


def pull(args):
    for src in args.board.walk():
        dest = args.dest / src.relative_to(args.board)
        print(f"{src} -> {dest}")
        if src.is_file():
            dest.write_bytes(src.read_bytes())
        elif src.is_dir():
            dest.mkdir(exist_ok=True, parents=True)
        # FIXME: mtime


parser = _top.subparsers.add_parser(
    'pull', help='Pull files from the board',
    parents=[_top.board_parser],
)
parser.add_argument('dest', help='Place to write files to', type=pathlib.Path)
parser.set_defaults(func=pull)
