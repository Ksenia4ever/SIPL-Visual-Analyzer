"""Tests for the SIPL command-line interface."""

import pytest

from sipl import __version__
from sipl.cli import main


def test_cli_info(capsys):
    exit_code = main(["info"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "SIPL Visual Analyzer" in captured.out
    assert __version__ in captured.out
    assert "Status: CLI available" in captured.out


def test_cli_help(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])

    captured = capsys.readouterr()

    assert exc_info.value.code == 0
    assert "Available commands" in captured.out
    assert "info" in captured.out


def test_cli_without_arguments(capsys):
    exit_code = main([])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "usage:" in captured.out


def test_cli_version(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])

    captured = capsys.readouterr()

    assert exc_info.value.code == 0
    assert __version__ in captured.out


def test_cli_unknown_command(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["unknown"])

    captured = capsys.readouterr()

    assert exc_info.value.code == 2
    assert "invalid choice" in captured.err
