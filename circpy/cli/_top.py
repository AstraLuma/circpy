import argparse

parser = argparse.ArgumentParser(
)

subparsers = parser.add_subparsers()

parser.set_defaults(func=lambda args: parser.print_help())
