"""Tests for the formal SIPL grammar (CORE-01)."""

import pytest

from sipl.syntax import (
    SIPLSyntaxError,
    get_parser,
    parse_source,
    validate_file,
    validate_source,
)


VALID_PROGRAMS = [
    # 1. Skip
    "begin skip end",

    # 2. Basic assignment
    "begin X := 0 end",

    # 3. Negative integer
    "begin X := -12 end",

    # 4. Arithmetic operations
    "begin X := 2 + 3 * 4 end",

    # 5. Arithmetic parentheses
    "begin X := (2 + 3) * 4 end",

    # 6. Sequential composition
    "begin X := 1; Y := X + 2 end",

    # 7. Conditional statement
    "begin if X = 0 then Y := 1 else Y := 2 end",

    # 8. While loop
    "begin while X > 0 do X := X - 1 end",

    # 9. Nested block and loop
    """
    begin
        X := 1;
        while X > 0 do
        begin
            X := X - 1;
            skip
        end
    end
    """,

    # 10. Logical negation and OR
    """
    begin
        if ¬ (X = 0 ∨ Y > 2)
        then skip
        else X := 3
    end
    """,

    # 11. Nested conditions
    """
    begin
        if X > 0 then
            if Y > 0 then skip else X := 1
        else X := 2
    end
    """,

    # 12. Unary minus and variables
    "begin X := 2; Y := -(X + 4) end",
]


INVALID_PROGRAMS = [
    # 1. Empty source
    "",

    # 2. Missing program wrapper
    "skip",

    # 3. Empty program body
    "begin end",

    # 4. Incorrect assignment operator
    "begin X = 1 end",

    # 5. Missing expression
    "begin X := end",

    # 6. Trailing semicolon
    "begin X := 1; end",

    # 7. Missing else branch
    "begin if X > 0 then skip end",

    # 8. Missing do keyword
    "begin while X > 0 X := X - 1 end",

    # 9. Unclosed parenthesis
    "begin X := (1 + 2 end",

    # 10. Unsupported division
    "begin X := 1 / 2 end",

    # 11. Unsupported comparison
    "begin if X < 3 then skip else skip end",

    # 12. Double semicolon
    "begin X := 1;; Y := 2 end",

    # 13. Invalid character
    "begin X := @ end",

    # 14. Missing block closure
    "begin while X > 0 do begin X := X - 1 end",
]


@pytest.mark.parametrize("source", VALID_PROGRAMS)
def test_valid_sipl_programs(source):
    assert validate_source(source) is True


@pytest.mark.parametrize("source", INVALID_PROGRAMS)
def test_invalid_sipl_programs(source):
    assert validate_source(source) is False


def test_parser_returns_tree():
    tree = parse_source("begin X := 1 end")

    assert tree.data == "start"
    assert tree.meta.line == 1
    assert tree.meta.column == 1


def test_syntax_error_has_location():
    source = "begin\nX := @\nend"

    with pytest.raises(SIPLSyntaxError) as exc_info:
        parse_source(source)

    error = exc_info.value

    assert error.line == 2
    assert error.column > 0
    assert "Invalid SIPL syntax" in str(error)
    assert "^" in str(error)


def test_valid_file(tmp_path):
    path = tmp_path / "valid.sipl"
    path.write_text("begin X := 5 end", encoding="utf-8")

    assert validate_file(str(path)) is True


def test_invalid_file(tmp_path):
    path = tmp_path / "invalid.sipl"
    path.write_text("begin X = 5 end", encoding="utf-8")

    assert validate_file(str(path)) is False


def test_parser_is_cached():
    assert get_parser() is get_parser()
