"""CLI orchestration unit testing."""

from unittest.mock import patch
from resume_generator.cli import GeneratorCLI


def test_fetch_fail_exits_with_1():
    """Test that a presumed failed fetch triggers a sys exit with code 1."""
    with patch("sys.exit") as mock_exit:
        with patch("resume_generator.cli.Fetcher.fetch") as mock_fetcher:
            mock_fetcher.return_value = False
            cli = GeneratorCLI("https://www.example.com")
            cli.fetch()
            mock_exit.assert_called_once_with(1)


@patch("resume_generator.cli.GeneratorCLI.generate")
@patch("resume_generator.cli.GeneratorCLI.tailor")
@patch("resume_generator.cli.GeneratorCLI.summarize")
@patch("resume_generator.cli.GeneratorCLI.fetch")
def test_all_calls(
    mock_cli_fetch, mock_cli_summarize, mock_cli_tailor, mock_cli_generate
):
    """Test that the cli.all method calls all corresponding methods in order"""
    cli = GeneratorCLI("https://www.example.com")
    cli.all()
    mock_cli_fetch.assert_called_once()
    mock_cli_summarize.assert_called_once()
    mock_cli_tailor.assert_called_once()
    mock_cli_generate.assert_called_once()
