"""Execution events built on top of the shared SIPL interpreter."""

from dataclasses import dataclass
from typing import Mapping

from sipl.ast import (
    Assignment,
    Block,
    Condition,
    Program,
    Sequence,
    SourceSpan,
    Statement,
)

from sipl.interpreter.runtime import (
    ExecutionResult,
    Interpreter,
)


@dataclass(frozen=True)
class TraceResult:
    state: dict[str, int]
    steps: int
    events: list[dict]


class TracingInterpreter(Interpreter):
    """Record source-linked events without duplicating evaluation."""

    def __init__(
        self,
        initial_state: Mapping[str, int] | None = None,
        max_steps: int = 10_000,
    ) -> None:
        super().__init__(
            initial_state=initial_state,
            max_steps=max_steps,
        )

        self.events: list[dict] = []

    def _record(
        self,
        event_type: str,
        span: SourceSpan,
        **details,
    ) -> None:
        self.events.append({
            "event_id": len(self.events) + 1,
            "type": event_type,
            "step": self.steps,
            "line": span.start_line,
            "column": span.start_column,
            "state": dict(sorted(self.state.items())),
            **details,
        })

    def _tick(self, span: SourceSpan) -> None:
        super()._tick(span)

        self._record(
            "step",
            span,
        )

    def _condition(self, condition: Condition) -> bool:
        result = super()._condition(condition)

        self._record(
            "condition_evaluated",
            condition.span,
            result=result,
        )

        return result

    def _statement(self, statement: Statement) -> None:
        if isinstance(statement, (Sequence, Block)):
            super()._statement(statement)
            return

        self._record(
            "before_statement",
            statement.span,
            statement=type(statement).__name__,
        )

        previous = (
            self.state.get(statement.name)
            if isinstance(statement, Assignment)
            else None
        )

        existed = (
            statement.name in self.state
            if isinstance(statement, Assignment)
            else False
        )

        super()._statement(statement)

        if isinstance(statement, Assignment):
            self._record(
                "variable_changed",
                statement.span,
                name=statement.name,
                old_value=previous if existed else None,
                new_value=self.state[statement.name],
            )

        self._record(
            "after_statement",
            statement.span,
            statement=type(statement).__name__,
        )

    def run_trace(self, program: Program) -> TraceResult:
        result: ExecutionResult = self.run(program)

        self._record(
            "completed",
            program.span,
        )

        return TraceResult(
            state=result.state,
            steps=result.steps,
            events=self.events.copy(),
        )


def trace_ast(
    program: Program,
    initial_state: Mapping[str, int] | None = None,
    max_steps: int = 10_000,
) -> TraceResult:
    return TracingInterpreter(
        initial_state=initial_state,
        max_steps=max_steps,
    ).run_trace(program)
