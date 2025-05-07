"""CLI orchestration unit testing."""

from unittest.mock import patch
from resume_generator.cli import GeneratorCLI

def test_fetch_success_sets_folder_name():
    """Test that a presumed succesfull fetch updates cli.folder_name correctly."""
    with patch('resume_generator.cli.Fetcher.fetch') as mock_fetcher:
        mock_fetcher.return_value = (True, "example.com")
        cli = GeneratorCLI()
        cli.fetch("https://www.example.com")
        assert cli.folder_name == "example.com"

def test_fetch_fail_exits_with_1():
    """Test that a presumed failed fetch triggers a sys exit with code 1."""
    with patch('sys.exit') as mock_exit:
        with patch('resume_generator.cli.Fetcher.fetch') as mock_fetcher:
            mock_fetcher.return_value = (False, "")
            cli = GeneratorCLI()
            cli.fetch("https://www.unreachable-website.com")
            mock_exit.assert_called_once_with(1)

def test_summarize_returns_summary_string():
    """Test that the summarizer returns a string summary on the cli because why not."""
    with patch('resume_generator.cli.Summarizer.summarize') as mock_summarizer:
        mock_summarizer.return_value = "AI generated job summary."
        cli = GeneratorCLI()
        summary = cli.summarize()
        assert summary == "AI generated job summary."

def test_tailor_returns_dict():
    """Test that the tailor returns a dictionary on the cli because why not."""
    with patch('resume_generator.cli.Tailor.tailor') as mock_tailor:
        mock_tailor.return_value = {"cv_data": "tailored_json"}
        cli = GeneratorCLI()
        tailored_data = cli.tailor("Job summary.")
        assert tailored_data == {"cv_data": "tailored_json"}

def test_generator_returns_generated_doc_path():
    """Test that the generator returns a string with the generated file path"""
    with patch('resume_generator.cli.Generator.generate') as mock_generate:
        mock_generate.return_value = "/valid/path/to/document.docx"
        cli = GeneratorCLI()
        summary = cli.generate({"tailored":"data"})
        assert summary == "/valid/path/to/document.docx"

@patch("resume_generator.cli.GeneratorCLI.generate")
@patch("resume_generator.cli.GeneratorCLI.tailor")
@patch("resume_generator.cli.GeneratorCLI.summarize")
@patch("resume_generator.cli.GeneratorCLI.fetch")
def test_all_calls(mock_cli_fetch, mock_cli_summarize, mock_cli_tailor, mock_cli_generate):
    """Test that the cli.all method calls all corresponding methods with valid parameters"""
    url, summary, tailored_data = "https://www.example.com", "AI summary.", {"d":1}
    cli = GeneratorCLI()
    mock_cli_summarize.return_value = summary
    mock_cli_tailor.return_value = tailored_data
    cli.all(url)
    mock_cli_fetch.assert_called_once_with(url)
    mock_cli_tailor.assert_called_once_with(summary)
    mock_cli_generate.assert_called_once_with(tailored_data)
