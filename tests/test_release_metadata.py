"""Release metadata and packaging readiness tests."""

from importlib.resources import files
from pathlib import Path
import tomllib

from sipl import __version__
from sipl.cli import main


ROOT = Path(__file__).resolve().parents[1]


def project_metadata():
    content = (
        ROOT / "pyproject.toml"
    ).read_bytes()

    return tomllib.loads(
        content.decode("utf-8")
    )


def test_release_version():
    assert __version__ == "1.0.0"


def test_project_version_matches_package():
    metadata = project_metadata()

    assert metadata["project"]["version"] == __version__


def test_package_grammar_available():
    grammar = (
        files("sipl")
        .joinpath("grammar.lark")
        .read_text(encoding="utf-8")
    )

    assert "start:" in grammar
    assert "assignment:" in grammar
    assert "loop:" in grammar


def test_license_exists_and_matches_metadata():
    metadata = project_metadata()

    license_text = (
        ROOT / "LICENSE"
    ).read_text(encoding="utf-8")

    assert metadata["project"]["license"] == "MIT"
    assert license_text.startswith("MIT License")
    assert "Permission is hereby granted" in license_text


def test_release_notes_exist():
    notes = (
        ROOT
        / "docs"
        / "RELEASE_NOTES_v1.0.0.md"
    ).read_text(encoding="utf-8")

    assert "v1.0.0" in notes
    assert "CORE-01" in notes
    assert "SEM-01" in notes


def test_cli_reports_release_version(capsys):
    from sipl.cli import main

    exit_code = main(["info"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "1.0.0" in output
