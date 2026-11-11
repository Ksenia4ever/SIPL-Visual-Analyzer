"""CORE-03 tests for SIPL execution semantics and runtime errors."""

from dataclasses import replace

import pytest

from sipl.ast import Statement
from sipl.interpreter import (
    SIPLRuntimeError,
    StepLimitExceededError,
    UndefinedVariableError,
    run_ast,
    run_file,
    run_source,
)
from sipl.parser import parse_ast
from sipl.syntax import SIPLSyntaxError


def test_assignment_and_state():
    result = run_source("begin X := 5 end")

    assert result.state == {"X": 5}
    assert result.steps == 1


def test_sequence_and_reassignment():
    result = run_source(
        "begin X := 2; Y := X + 3; X := Y * 2 end"
    )

    assert result.state == {"X": 10, "Y": 5}
    assert result.steps == 3


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("begin X := 2 + 3 * 4 end", 14),
        ("begin X := (2 + 3) * 4 end", 20),
        ("begin X := 10 - 3 - 2 end", 5),
        ("begin X := -7 end", -7),
        ("begin X := -(2 + 3) * -2 end", 10),
    ],
)
def test_arithmetic(source, expected):
    assert run_source(source).state["X"] == expected


def test_skip():
    result = run_source("begin skip end")

    assert result.state == {}
    assert result.steps == 1


def test_nested_blocks():
    result = run_source(
        "begin X := 1; begin X := X + 1; skip end end"
    )

    assert result.state == {"X": 2}
    assert result.steps == 3


@pytest.mark.parametrize(
    ("initial", "expected"),
    [
        (5, 1),
        (0, 2),
        (-1, 2),
    ],
)
def test_if_else(initial, expected):
    result = run_source(
        "begin if X > 0 then Y := 1 else Y := 2 end",
        initial_state={"X": initial},
    )

    assert result.state == {
        "X": initial,
        "Y": expected,
    }
    assert result.steps == 2


def test_equality():
    source = (
        "begin if X = 2 then Y := 3 else Y := 4 end"
    )

    assert run_source(source, {"X": 2}).state["Y"] == 3
    assert run_source(source, {"X": 5}).state["Y"] == 4


def test_logical_or_and_not():
    source = (
        "begin "
        "if ¬ (X = 0 ∨ Y > 2) "
        "then R := 1 else R := 0 "
        "end"
    )

    assert run_source(
        source, {"X": 1, "Y": 1}
    ).state["R"] == 1

    assert run_source(
        source, {"X": 0, "Y": 1}
    ).state["R"] == 0

    assert run_source(
        source, {"X": 1, "Y": 3}
    ).state["R"] == 0


def test_logical_or_short_circuit():
    source = (
        "begin "
        "if X = 0 ∨ MISSING > 0 "
        "then R := 1 else R := 0 "
        "end"
    )

    result = run_source(source, {"X": 0})

    assert result.state["R"] == 1


def test_while_loop_sum():
    source = (
        "begin "
        "X := 3; R := 0; "
        "while X > 0 do "
        "begin "
        "R := R + X; "
        "X := X - 1 "
        "end "
        "end"
    )

    result = run_source(source)

    assert result.state == {
        "X": 0,
        "R": 6,
    }

    assert result.steps == 12


def test_while_zero_iterations():
    result = run_source(
        "begin while X > 0 do X := X - 1 end",
        {"X": 0},
    )

    assert result.state == {"X": 0}
    assert result.steps == 1


def test_nested_if_while():
    source = (
        "begin "
        "X := 2; R := 0; "
        "while X > 0 do "
        "begin "
        "if X = 2 then "
        "R := R + 10 "
        "else R := R + 1; "
        "X := X - 1 "
        "end "
        "end"
    )

    result = run_source(source)

    assert result.state == {
        "X": 0,
        "R": 11,
    }


def test_initial_state_not_mutated():
    initial = {"X": 4}

    result = run_source(
        "begin X := X + 1 end",
        initial,
    )

    assert result.state == {"X": 5}
    assert initial == {"X": 4}


def test_undefined_variable_error_position():
    source = "begin\n  X := Y + 1\nend"

    with pytest.raises(UndefinedVariableError) as exc:
        run_source(source)

    assert exc.value.span.start_line == 2
    assert "Undefined variable 'Y'" in str(exc.value)
    assert "column 8" in str(exc.value)


def test_undefined_variable_in_condition():
    with pytest.raises(UndefinedVariableError):
        run_source(
            "begin if X > 0 then skip else skip end"
        )


def test_loop_step_limit():
    source = (
        "begin "
        "X := 1; "
        "while X > 0 do skip "
        "end"
    )

    with pytest.raises(
        StepLimitExceededError
    ) as exc:
        run_source(source, max_steps=5)

    assert "step limit (5)" in str(exc.value)


def test_exact_limit_and_limit_one():
    result = run_source(
        "begin X := 1 end",
        max_steps=1,
    )

    assert result.steps == 1

    with pytest.raises(StepLimitExceededError):
        run_source(
            "begin skip; skip end",
            max_steps=1,
        )


@pytest.mark.parametrize(
    "limit",
    [0, -1, 1.5, True],
)
def test_invalid_step_limits(limit):
    with pytest.raises(
        ValueError,
        match="max_steps",
    ):
        run_source(
            "begin skip end",
            max_steps=limit,
        )


@pytest.mark.parametrize(
    "initial",
    [
        {"X": 3.4},
        {"X": True},
        {10: 2},
    ],
)
def test_invalid_initial_states(initial):
    with pytest.raises(
        ValueError,
        match="initial_state",
    ):
        run_source(
            "begin skip end",
            initial_state=initial,
        )


def test_file_execution(tmp_path):
    path = tmp_path / "program.sipl"

    path.write_text(
        "begin X := 4; X := X * 3 end",
        encoding="utf-8",
    )

    result = run_file(path)

    assert result.state == {"X": 12}


def test_run_ast():
    ast = parse_ast("begin X := 3 end")

    result = run_ast(ast)

    assert result.state == {"X": 3}


def test_invalid_syntax_is_reported():
    with pytest.raises(SIPLSyntaxError):
        run_source("begin X = 2 end")


def test_unsupported_arithmetic_operator_is_guarded():
    ast = parse_ast("begin X := 2 + 3 end")

    assignment = ast.body.statements[0]

    invalid = replace(
        assignment.value,
        operator="/",
    )

    new_assignment = replace(
        assignment,
        value=invalid,
    )

    new_body = replace(
        ast.body,
        statements=(new_assignment,),
    )

    with pytest.raises(
        SIPLRuntimeError,
        match="Unsupported arithmetic",
    ):
        run_ast(replace(ast, body=new_body))


def test_unsupported_comparison_operator_is_guarded():
    ast = parse_ast(
        "begin if X = 1 then skip else skip end"
    )

    statement = ast.body.statements[0]

    bad = replace(
        statement.condition,
        operator="<",
    )

    new_statement = replace(
        statement,
        condition=bad,
    )

    new_body = replace(
        ast.body,
        statements=(new_statement,),
    )

    with pytest.raises(
        SIPLRuntimeError,
        match="Unsupported Boolean",
    ):
        run_ast(
            replace(ast, body=new_body),
            {"X": 1},
        )


def test_unsupported_statement_is_guarded():
    ast = parse_ast("begin skip end")

    class Unsupported(Statement):
        pass

    new_body = replace(
        ast.body,
        statements=(
            Unsupported(span=ast.body.span),
        ),
    )

    with pytest.raises(
        SIPLRuntimeError,
        match="Unsupported statement",
    ):
        run_ast(replace(ast, body=new_body))
