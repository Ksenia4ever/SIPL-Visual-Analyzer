"""Execution engine for the core SIPL language."""

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from sipl.ast import (
    Assignment,
    BinaryExpression,
    Block,
    Comparison,
    Condition,
    Expression,
    IfStatement,
    IntegerLiteral,
    LogicalNot,
    LogicalOr,
    Program,
    Sequence,
    Skip,
    SourceSpan,
    Statement,
    UnaryMinus,
    Variable,
    WhileStatement,
)
from sipl.parser import parse_ast


class SIPLRuntimeError(Exception):
    """A runtime error related to a position in SIPL source code."""

    def __init__(self, message: str, span: SourceSpan) -> None:
        self.message = message
        self.span = span
        super().__init__(
            f"{message} at line {span.start_line}, "
            f"column {span.start_column}"
        )


class UndefinedVariableError(SIPLRuntimeError):
    """Raised if a variable is read before it has a value."""


class StepLimitExceededError(SIPLRuntimeError):
    """Raised when a program exceeds its execution step limit."""


@dataclass(frozen=True)
class ExecutionResult:
    """Final variable state and the number of consumed execution steps."""

    state: dict[str, int]
    steps: int


class Interpreter:
    """Executes the typed AST of a SIPL program."""

    def __init__(
        self,
        initial_state: Mapping[str, int] | None = None,
        max_steps: int = 10_000,
    ) -> None:
        if type(max_steps) is not int or max_steps <= 0:
            raise ValueError("max_steps must be a positive integer")

        state = dict(initial_state) if initial_state is not None else {}

        for name, value in state.items():
            if not isinstance(name, str) or type(value) is not int:
                raise ValueError(
                    "initial_state must map variable names to integers"
                )

        self.state = state
        self.max_steps = max_steps
        self.steps = 0

    def _tick(self, span: SourceSpan) -> None:
        """Count an assignment, skip, if evaluation, or while condition."""

        if self.steps >= self.max_steps:
            raise StepLimitExceededError(
                f"Execution step limit ({self.max_steps}) exceeded",
                span,
            )

        self.steps += 1

    def _expression(self, expression: Expression) -> int:
        """Evaluate an arithmetic expression."""

        if isinstance(expression, IntegerLiteral):
            return expression.value

        if isinstance(expression, Variable):
            if expression.name not in self.state:
                raise UndefinedVariableError(
                    f"Undefined variable '{expression.name}'",
                    expression.span,
                )

            return self.state[expression.name]

        if isinstance(expression, UnaryMinus):
            return -self._expression(expression.operand)

        if isinstance(expression, BinaryExpression):
            left = self._expression(expression.left)
            right = self._expression(expression.right)

            if expression.operator == "+":
                return left + right

            if expression.operator == "-":
                return left - right

            if expression.operator == "*":
                return left * right

        raise SIPLRuntimeError(
            "Unsupported arithmetic expression",
            expression.span,
        )

    def _condition(self, condition: Condition) -> bool:
        """Evaluate a Boolean SIPL condition."""

        if isinstance(condition, Comparison):
            left = self._expression(condition.left)
            right = self._expression(condition.right)

            if condition.operator == "=":
                return left == right

            if condition.operator == ">":
                return left > right

        elif isinstance(condition, LogicalNot):
            return not self._condition(condition.operand)

        elif isinstance(condition, LogicalOr):
            # Logical OR uses short-circuit evaluation.
            return (
                self._condition(condition.left)
                or self._condition(condition.right)
            )

        raise SIPLRuntimeError(
            "Unsupported Boolean condition",
            condition.span,
        )

    def _statement(self, statement: Statement) -> None:
        """Execute one statement or a statement structure."""

        if isinstance(statement, Sequence):
            for child in statement.statements:
                self._statement(child)

        elif isinstance(statement, Block):
            self._statement(statement.body)

        elif isinstance(statement, Assignment):
            self._tick(statement.span)

            self.state[statement.name] = self._expression(
                statement.value
            )

        elif isinstance(statement, Skip):
            self._tick(statement.span)

        elif isinstance(statement, IfStatement):
            self._tick(statement.span)

            branch = (
                statement.then_branch
                if self._condition(statement.condition)
                else statement.else_branch
            )

            self._statement(branch)

        elif isinstance(statement, WhileStatement):
            while True:
                self._tick(statement.span)

                if not self._condition(statement.condition):
                    break

                self._statement(statement.body)

        else:
            raise SIPLRuntimeError(
                "Unsupported statement",
                statement.span,
            )

    def run(self, program: Program) -> ExecutionResult:
        """Execute the program and return a final state snapshot."""

        self._statement(program.body)

        return ExecutionResult(
            state=self.state.copy(),
            steps=self.steps,
        )


def run_ast(
    program: Program,
    initial_state: Mapping[str, int] | None = None,
    max_steps: int = 10_000,
) -> ExecutionResult:
    """Execute an already parsed SIPL AST."""

    return Interpreter(
        initial_state=initial_state,
        max_steps=max_steps,
    ).run(program)


def run_source(
    source: str,
    initial_state: Mapping[str, int] | None = None,
    max_steps: int = 10_000,
) -> ExecutionResult:
    """Parse and execute SIPL source code."""

    return run_ast(
        parse_ast(source),
        initial_state,
        max_steps,
    )


def run_file(
    path: str | Path,
    initial_state: Mapping[str, int] | None = None,
    max_steps: int = 10_000,
) -> ExecutionResult:
    """Read and execute a UTF-8 SIPL file."""

    source = Path(path).read_text(encoding="utf-8-sig")

    return run_source(
        source,
        initial_state,
        max_steps,
    )
