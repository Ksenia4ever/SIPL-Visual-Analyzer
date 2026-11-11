"""Command line interface for SIPL Visual Analyzer."""

import argparse
from dataclasses import fields, is_dataclass
import json
from pathlib import Path
import re
import sys

from sipl import __version__
from sipl.ast import SourceSpan

from sipl.interpreter import (
    SIPLRuntimeError,
    run_ast,
    trace_ast,
)

from sipl.parser import parse_ast
from sipl.syntax import SIPLSyntaxError


SCHEMA_VERSION = "1.0"

_IDENTIFIER = re.compile(
    r"(?!begin$|end$|if$|then$|else$|while$|do$|skip$)"
    r"[A-Za-z][A-Za-z0-9_]*\Z"
)


def _positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "must be a positive integer"
        ) from exc

    if number <= 0:
        raise argparse.ArgumentTypeError(
            "must be a positive integer"
        )

    return number


def _state_assignment(value: str) -> tuple[str, int]:
    name, separator, number = value.partition("=")

    if (
        not separator
        or not _IDENTIFIER.fullmatch(name)
        or not re.fullmatch(r"-?[0-9]+", number)
    ):
        raise argparse.ArgumentTypeError(
            "state must be NAME=INTEGER (example: X=-3)"
        )

    return name, int(number)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sipl",
        description="SIPL Visual Analyzer",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"SIPL Visual Analyzer {__version__}",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="Available commands",
    )

    subparsers.add_parser(
        "info",
        help="Show information about the project",
    )

    commands = (
        ("check", "Validate SIPL source code"),
        ("parse", "Display the typed SIPL AST"),
        ("run", "Execute a SIPL program"),
        ("trace", "Execute a SIPL program with events"),
    )

    for name, description in commands:
        subparser = subparsers.add_parser(
            name,
            help=description,
        )

        subparser.add_argument(
            "file",
            help="Path to a .sipl file",
        )

        subparser.add_argument(
            "--json",
            action="store_true",
            dest="json_output",
            help="Emit stable JSON envelope",
        )

        if name in ("run", "trace"):
            subparser.add_argument(
                "--state",
                action="append",
                type=_state_assignment,
                default=[],
                metavar="NAME=INTEGER",
                help="Initial variable (repeatable)",
            )

            subparser.add_argument(
                "--max-steps",
                type=_positive_int,
                default=10_000,
                metavar="N",
                help="Maximum execution steps",
            )

    return parser


def _ast_data(value):
    if isinstance(value, SourceSpan):
        return {
            field.name: getattr(value, field.name)
            for field in fields(value)
        }

    if is_dataclass(value):
        return {
            "node_type": type(value).__name__,
            **{
                field.name: _ast_data(
                    getattr(value, field.name)
                )
                for field in fields(value)
            },
        }

    if isinstance(value, (list, tuple)):
        return [
            _ast_data(item)
            for item in value
        ]

    return value


def _print_ast(value, indent: int = 0) -> None:
    prefix = "  " * indent

    print(
        f"{prefix}{type(value).__name__} "
        f"[{value.span.start_line}:"
        f"{value.span.start_column}]"
    )

    for field in fields(value):
        if field.name == "span":
            continue

        child = getattr(value, field.name)

        if is_dataclass(child):
            print(f"{prefix}  {field.name}:")
            _print_ast(child, indent + 2)

        elif isinstance(child, (list, tuple)):
            print(f"{prefix}  {field.name}:")

            for item in child:
                _print_ast(item, indent + 2)

        else:
            print(
                f"{prefix}  {field.name}: {child!r}"
            )


def _emit(
    command: str,
    data: dict | None,
    error: dict | None,
    json_output: bool,
) -> None:
    if json_output:
        print(
            json.dumps(
                {
                    "schema_version": SCHEMA_VERSION,
                    "command": command,
                    "ok": error is None,
                    "data": data,
                    "error": error,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return

    if error is not None:
        print(
            f"Error [{error['code']}]: "
            f"{error['message']}",
            file=sys.stderr,
        )
        return

    if command == "check":
        print("Syntax OK: valid SIPL program")

    elif command == "parse":
        _print_ast(data["ast_object"])

    elif command == "run":
        print(
            "Execution completed successfully.\n"
            "\nFinal state:"
        )

        for name, value in data["state"].items():
            print(f"  {name} = {value}")

        print(f"\nSteps: {data['steps']}")

    elif command == "trace":
        for event in data["events"]:
            details = ""

            if event["type"] == "condition_evaluated":
                details = f" result={event['result']}"

            elif event["type"] == "variable_changed":
                details = (
                    f" {event['name']}: "
                    f"{event['old_value']} -> "
                    f"{event['new_value']}"
                )

            print(
                f"[{event['event_id']:03}] "
                f"step={event['step']} "
                f"{event['type']} "
                f"at {event['line']}:{event['column']}"
                f"{details}"
            )

        print(f"Final state: {data['state']}")
        print(f"Steps: {data['steps']}")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "info":
        print("SIPL Visual Analyzer")
        print(f"Version: {__version__}")
        print("Language: SIPL")
        print("Status: CLI available")
        return 0

    if args.command is None:
        parser.print_help()
        return 0

    command = args.command
    json_output = args.json_output

    try:
        source = Path(args.file).read_text(
            encoding="utf-8-sig"
        )

        program = parse_ast(source)

        if command == "check":
            data = {
                "valid": True,
            }

        elif command == "parse":
            data = {
                "ast": _ast_data(program),
            }

        else:
            initial = {}

            for name, value in args.state:
                if name in initial:
                    parser.error(
                        f"duplicate initial variable: {name}"
                    )

                initial[name] = value

            if command == "run":
                result = run_ast(
                    program,
                    initial_state=initial,
                    max_steps=args.max_steps,
                )

                data = {
                    "state": dict(
                        sorted(result.state.items())
                    ),
                    "steps": result.steps,
                }

            else:
                result = trace_ast(
                    program,
                    initial_state=initial,
                    max_steps=args.max_steps,
                )

                data = {
                    "state": dict(
                        sorted(result.state.items())
                    ),
                    "steps": result.steps,
                    "events": result.events,
                }

        if command == "parse" and not json_output:
            data = {
                "ast_object": program,
            }

        _emit(
            command,
            data,
            None,
            json_output,
        )

        return 0

    except SIPLSyntaxError as error:
        _emit(
            command,
            None,
            {
                "code": "SYNTAX_ERROR",
                "message": str(error),
                "line": error.line,
                "column": error.column,
            },
            json_output,
        )

        return 1

    except SIPLRuntimeError as error:
        _emit(
            command,
            None,
            {
                "code": "RUNTIME_ERROR",
                "message": str(error),
                "line": error.span.start_line,
                "column": error.span.start_column,
            },
            json_output,
        )

        return 3

    except (OSError, UnicodeError) as error:
        _emit(
            command,
            None,
            {
                "code": "FILE_ERROR",
                "message": str(error),
                "line": None,
                "column": None,
            },
            json_output,
        )

        return 4


if __name__ == "__main__":
    raise SystemExit(main())
