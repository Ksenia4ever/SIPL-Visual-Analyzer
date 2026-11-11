"""Command-line interface for SIPL Visual Analyzer."""

import argparse

from sipl import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sipl",
        description="SIPL Visual Analyzer"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"SIPL Visual Analyzer {__version__}"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="Available commands"
    )

    subparsers.add_parser(
        "info",
        help="Show information about the project"
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "info":
        print("SIPL Visual Analyzer")
        print(f"Version: {__version__}")
        print("Language: SIPL")
        print("Status: Project initialization")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
