"""Integration tests for the SIPL command-line interface."""

import json
import subprocess
import sys

import pytest


def invoke(*args):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "sipl.cli",
            *map(str, args),
        ],
        text=True,
        capture_output=True,
        check=False,
    )


@pytest.fixture
def valid_path(tmp_path):
    path = tmp_path / "valid.sipl"

    path.write_text(
        "begin X := 2; while X > 0 do X := X - 1 end",
        encoding="utf-8",
    )

    return path


@pytest.fixture
def invalid_path(tmp_path):
    path = tmp_path / "invalid.sipl"

    path.write_text(
        "begin X = 2 end",
        encoding="utf-8",
    )

    return path


def payload(process):
    return json.loads(process.stdout)


def test_check_valid_json(valid_path):
    result = invoke("check", valid_path, "--json")

    assert result.returncode == 0

    assert payload(result) == {
        "schema_version": "1.0",
        "command": "check",
        "ok": True,
        "data": {"valid": True},
        "error": None,
    }


def test_check_invalid_json(invalid_path):
    result = invoke("check", invalid_path, "--json")

    assert result.returncode == 1

    body = payload(result)

    assert body["command"] == "check"
    assert body["ok"] is False
    assert body["error"]["code"] == "SYNTAX_ERROR"
    assert body["error"]["line"] == 1
    assert body["error"]["column"] > 0


def test_check_text(valid_path):
    result = invoke("check", valid_path)

    assert result.returncode == 0
    assert "Syntax OK" in result.stdout


def test_parse_json(valid_path):
    result = invoke("parse", valid_path, "--json")

    assert result.returncode == 0

    ast = payload(result)["data"]["ast"]

    assert ast["node_type"] == "Program"
    assert ast["body"]["node_type"] == "Sequence"
    assert ast["span"]["start_line"] == 1


def test_parse_text(valid_path):
    result = invoke("parse", valid_path)

    assert result.returncode == 0
    assert "Program" in result.stdout
    assert "WhileStatement" in result.stdout


def test_run_json(valid_path):
    result = invoke("run", valid_path, "--json")

    assert result.returncode == 0

    assert payload(result)["data"] == {
        "state": {"X": 0},
        "steps": 6,
    }


def test_run_text(valid_path):
    result = invoke("run", valid_path)

    assert result.returncode == 0
    assert "X = 0" in result.stdout
    assert "Steps: 6" in result.stdout


def test_trace_events_json(valid_path):
    result = invoke("trace", valid_path, "--json")

    assert result.returncode == 0

    body = payload(result)["data"]

    assert body["state"] == {"X": 0}
    assert body["steps"] == 6

    events = body["events"]

    assert events[0]["type"] == "before_statement"
    assert events[-1]["type"] == "completed"

    assert [
        event["event_id"]
        for event in events
    ] == list(range(1, len(events) + 1))

    changes = [
        event["new_value"]
        for event in events
        if event["type"] == "variable_changed"
    ]

    assert changes == [2, 1, 0]

    assert any(
        event["type"] == "condition_evaluated"
        and event["result"] is False
        for event in events
    )

    assert all(
        "line" in event
        and "column" in event
        and "state" in event
        for event in events
    )


def test_trace_text(valid_path):
    result = invoke("trace", valid_path)

    assert result.returncode == 0
    assert "variable_changed" in result.stdout
    assert "completed" in result.stdout


def test_run_initial_state(tmp_path):
    path = tmp_path / "initial.sipl"

    path.write_text(
        "begin R := X * 2 end",
        encoding="utf-8",
    )

    result = invoke(
        "run",
        path,
        "--state",
        "X=5",
        "--json",
    )

    assert result.returncode == 0

    assert payload(result)["data"]["state"] == {
        "R": 10,
        "X": 5,
    }


def test_runtime_error_json(tmp_path):
    path = tmp_path / "runtime.sipl"

    path.write_text(
        "begin R := X end",
        encoding="utf-8",
    )

    result = invoke("run", path, "--json")

    assert result.returncode == 3

    error = payload(result)["error"]

    assert error["code"] == "RUNTIME_ERROR"
    assert "Undefined variable" in error["message"]


def test_step_limit_json(tmp_path):
    path = tmp_path / "loop.sipl"

    path.write_text(
        "begin X := 1; while X > 0 do skip end",
        encoding="utf-8",
    )

    result = invoke(
        "trace",
        path,
        "--max-steps",
        "4",
        "--json",
    )

    assert result.returncode == 3

    assert (
        payload(result)["error"]["code"]
        == "RUNTIME_ERROR"
    )


def test_missing_file_json(tmp_path):
    result = invoke(
        "check",
        tmp_path / "missing.sipl",
        "--json",
    )

    assert result.returncode == 4

    assert (
        payload(result)["error"]["code"]
        == "FILE_ERROR"
    )


@pytest.mark.parametrize(
    "args",
    [
        ("--state", "X"),
        ("--state", "X=yes"),
        ("--state", "if=1"),
        ("--max-steps", "0"),
        ("--max-steps", "abc"),
    ],
)
def test_invalid_arguments(valid_path, args):
    result = invoke(
        "run",
        valid_path,
        *args,
    )

    assert result.returncode == 2
    assert "error:" in result.stderr


def test_duplicate_variable(valid_path):
    result = invoke(
        "run",
        valid_path,
        "--state",
        "X=1",
        "--state",
        "X=2",
    )

    assert result.returncode == 2
    assert "duplicate" in result.stderr


def test_no_json_errors_on_stderr(invalid_path):
    result = invoke("parse", invalid_path)

    assert result.returncode == 1
    assert "SYNTAX_ERROR" in result.stderr


def test_utf8_bom_support(tmp_path):
    path = tmp_path / "bom.sipl"

    path.write_text(
        "begin skip end",
        encoding="utf-8-sig",
    )

    result = invoke("check", path, "--json")

    assert result.returncode == 0


def test_repeated_distinct_initial_values(tmp_path):
    path = tmp_path / "params.sipl"

    path.write_text(
        "begin R := X + Y end",
        encoding="utf-8",
    )

    result = invoke(
        "run",
        path,
        "--state",
        "X=-2",
        "--state",
        "Y=8",
        "--json",
    )

    assert result.returncode == 0

    assert payload(result)["data"]["state"] == {
        "R": 6,
        "X": -2,
        "Y": 8,
    }
