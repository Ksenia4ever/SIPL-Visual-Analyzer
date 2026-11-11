"""Syntax analysis for the SIPL programming language."""

from functools import lru_cache
from importlib.resources import files

from lark import Lark, Tree
from lark.exceptions import UnexpectedInput


class SIPLSyntaxError(Exception):
    """A syntax error with a source location."""

    def __init__(
        self,
        message: str,
        line: int,
        column: int,
        source_line: str = "",
    ) -> None:
        self.message = message
        self.line = line
        self.column = column
        self.source_line = source_line

        location = f"line {line}, column {column}"

        if source_line:
            pointer = " " * (column - 1) + "^"
            details = (
                f"{message} at {location}\n"
                f"{source_line}\n"
                f"{pointer}"
            )
        else:
            details = f"{message} at {location}"

        super().__init__(details)


@lru_cache(maxsize=1)
def get_parser() -> Lark:
    """Load the packaged SIPL grammar and create a parser."""

    grammar = (
        files("sipl")
        .joinpath("grammar.lark")
        .read_text(encoding="utf-8")
    )

    return Lark(
        grammar,
        parser="lalr",
        lexer="contextual",
        start="start",
        propagate_positions=True,
        maybe_placeholders=False,
    )


def parse_source(source: str) -> Tree:
    """Parse SIPL source code into a Lark concrete parse tree.

    A typed AST will be implemented in CORE-02.
    """

    parser = get_parser()

    try:
        return parser.parse(source)

    except UnexpectedInput as error:
        line = getattr(error, "line", 1) or 1
        column = getattr(error, "column", 1) or 1

        source_lines = source.splitlines()
        source_line = ""

        if 1 <= line <= len(source_lines):
            source_line = source_lines[line - 1]

        raise SIPLSyntaxError(
            message="Invalid SIPL syntax",
            line=line,
            column=column,
            source_line=source_line,
        ) from error


def validate_source(source: str) -> bool:
    """Return True if the source is a valid SIPL program."""

    try:
        parse_source(source)
        return True
    except SIPLSyntaxError:
        return False


def validate_file(path: str) -> bool:
    """Validate a SIPL program stored in a UTF-8 file."""

    with open(path, "r", encoding="utf-8-sig") as file:
        source = file.read()

    return validate_source(source)
