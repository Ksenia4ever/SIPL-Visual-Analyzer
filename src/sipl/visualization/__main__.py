"""Visualize SIPL parse trees from the command line."""

import argparse
from pathlib import Path
import sys

from sipl.syntax import SIPLSyntaxError

from .tree import (
    parse_cst,
    tree_to_dot,
    tree_to_json,
    tree_to_text,
    write_svg,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m sipl.visualization",
        description=(
            "Export a SIPL concrete parse tree "
            "with source positions"
        ),
    )

    parser.add_argument(
        "file",
        help="Source .sipl file",
    )

    parser.add_argument(
        "--format",
        choices=("text", "json", "dot", "svg", "all"),
        default="text",
        help="Output representation (default: text)",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help=(
            "Output file, or directory "
            "for --format all"
        ),
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if (
        args.format in {"svg", "all"}
        and args.output is None
    ):
        print(
            "Error: --output is required "
            "for svg and all formats",
            file=sys.stderr,
        )
        return 2

    try:
        source = Path(args.file).read_text(
            encoding="utf-8-sig"
        )

        tree = parse_cst(source)

        if args.format == "all":
            directory = args.output

            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            name = Path(args.file).stem

            formats = (
                ("txt", tree_to_text(tree)),
                ("json", tree_to_json(tree)),
                ("dot", tree_to_dot(tree)),
            )

            for extension, content in formats:
                destination = (
                    directory
                    / f"{name}.cst.{extension}"
                )

                destination.write_text(
                    content,
                    encoding="utf-8",
                )

            write_svg(
                tree,
                directory / f"{name}.cst.svg",
            )

            print(
                f"Created CST exports in: {directory}"
            )

            return 0

        if args.format == "svg":
            write_svg(tree, args.output)

            print(
                f"Created SVG: {args.output}"
            )

            return 0

        exporters = {
            "text": tree_to_text,
            "json": tree_to_json,
            "dot": tree_to_dot,
        }

        content = exporters[args.format](tree)

        if args.output is None:
            print(
                content,
                end="" if content.endswith("\n") else "\n",
            )

        else:
            args.output.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            args.output.write_text(
                content,
                encoding="utf-8",
            )

            print(
                f"Created {args.format}: {args.output}"
            )

        return 0

    except SIPLSyntaxError as error:
        print(
            f"Syntax error: {error}",
            file=sys.stderr,
        )
        return 1

    except (OSError, UnicodeError) as error:
        print(
            f"File error: {error}",
            file=sys.stderr,
        )
        return 4

    except RuntimeError as error:
        print(
            f"Visualization error: {error}",
            file=sys.stderr,
        )
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
