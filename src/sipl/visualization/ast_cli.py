"""CLI for VIS-02 AST visualization and CST/AST comparisons."""

import argparse
from pathlib import Path
import sys

from sipl.parser import parse_ast
from sipl.syntax import SIPLSyntaxError

from sipl.visualization.ast_tree import (
    ast_to_dot,
    ast_to_json,
    ast_to_text,
    comparison_json,
    write_ast_svg,
    write_comparison_html,
)
from sipl.visualization.tree import parse_cst


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m sipl.visualization.ast_cli",
        description=(
            "VIS-02: export SIPL AST "
            "and compare AST vs CST"
        ),
    )

    parser.add_argument(
        "file",
        help="SIPL source file",
    )

    parser.add_argument(
        "--format",
        choices=(
            "text",
            "json",
            "dot",
            "svg",
            "compare",
            "compare-json",
            "all",
        ),
        default="text",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output file or directory for all",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if (
        args.format in ("svg", "compare", "all")
        and args.output is None
    ):
        print(
            "Error: --output is required "
            "for svg, compare, and all",
            file=sys.stderr,
        )
        return 2

    try:
        source = Path(args.file).read_text(
            encoding="utf-8-sig"
        )

        program = parse_ast(source)

        if args.format == "all":
            directory = args.output

            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            stem = Path(args.file).stem

            exports = {
                "txt": ast_to_text(program),
                "json": ast_to_json(program),
                "dot": ast_to_dot(program),
            }

            for extension, content in exports.items():
                destination = (
                    directory
                    / f"{stem}.ast.{extension}"
                )

                destination.write_text(
                    content,
                    encoding="utf-8",
                )

            write_ast_svg(
                program,
                directory / f"{stem}.ast.svg",
            )

            cst = parse_cst(source)

            (
                directory / f"{stem}.comparison.json"
            ).write_text(
                comparison_json(program, cst),
                encoding="utf-8",
            )

            write_comparison_html(
                program,
                cst,
                source,
                directory / f"{stem}.comparison.html",
                Path(args.file).name,
            )

            print(
                "Created AST and comparison "
                f"exports in: {directory}"
            )

            return 0

        if args.format == "svg":
            write_ast_svg(
                program,
                args.output,
            )

            print(
                f"Created AST SVG: {args.output}"
            )

            return 0

        if args.format == "compare":
            cst = parse_cst(source)

            write_comparison_html(
                program,
                cst,
                source,
                args.output,
                Path(args.file).name,
            )

            print(
                "Created comparison HTML: "
                f"{args.output}"
            )

            return 0

        exporters = {
            "text": ast_to_text,
            "json": ast_to_json,
            "dot": ast_to_dot,
        }

        if args.format == "compare-json":
            content = comparison_json(
                program,
                parse_cst(source),
            )
        else:
            content = exporters[args.format](
                program
            )

        if args.output is None:
            print(
                content,
                end=(
                    "" if content.endswith("\n")
                    else "\n"
                ),
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
