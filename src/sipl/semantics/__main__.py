"""SEM-01: create a formal semantic term for a SIPL program."""

import argparse
import json
from pathlib import Path
import sys

from sipl.parser import parse_ast
from sipl.syntax import SIPLSyntaxError

from .terms import (
    build_term,
    format_term,
    term_to_data,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Construct a SIPL semantic term"
    )

    parser.add_argument(
        "file",
        type=Path,
        help="Source SIPL file",
    )

    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Write result to a UTF-8 file",
    )

    args = parser.parse_args(argv)

    try:
        source = args.file.read_text(
            encoding="utf-8-sig"
        )

        term = build_term(
            parse_ast(source)
        )

        rendered = format_term(term)

        if args.format == "json":
            content = json.dumps(
                {
                    "schema_version": "1.0",
                    "notation": "ASIPL",
                    "term": rendered,
                    "structure": term_to_data(term),
                },
                ensure_ascii=False,
                indent=2,
            ) + "\n"

        else:
            content = rendered + "\n"

        if args.output is None:
            print(
                content,
                end="",
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
                f"Created semantic term: {args.output}"
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

    except (TypeError, ValueError) as error:
        print(
            f"Semantic error: {error}",
            file=sys.stderr,
        )

        return 5


if __name__ == "__main__":
    # Explicit UTF-8 avoids encoding problems with Unicode
    # mathematical symbols in redirected Windows output.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    raise SystemExit(main())
