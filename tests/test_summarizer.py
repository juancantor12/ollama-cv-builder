"""
Tests for the summarizer submodule.
The following functions are not covered because they are too trivial:
    - save_ollama_job_summary
    - get_ollama_summary
"""

from unittest.mock import patch
from resume_generator.summarizer import Summarizer


@patch("builtins.open")
@patch("resume_generator.utils.Utils.get_output_path")
def test_get_raw_offering_data(mock_get_output_path, mock_open):
    """Test succesfully opening a file."""
    mock_get_output_path.return_value = "/out/path"
    test_data = "File data"
    folder_name = "example.com"
    mocked_file = mock_open.return_value
    mock_read = (
        mocked_file.__enter__.return_value.read
    )  # __enter__ because of "with" opening
    mock_read.return_value = test_data
    summarizer = Summarizer(folder_name)
    raw_data = summarizer.get_raw_offering_data()
    mock_get_output_path.assert_called_once_with(folder_name)
    mock_open.assert_called_once_with(
        "/out/path/html_free_job_details.txt", "r", encoding="utf-8"
    )
    assert raw_data == test_data


@patch("resume_generator.summarizer.Summarizer.save_ollama_job_summary")
@patch("resume_generator.summarizer.Summarizer.get_ollama_summary")
@patch("resume_generator.summarizer.Summarizer.get_raw_offering_data")
def test_summarize(
    mock_get_raw_offering_data, mock_get_ollama_summary, mock_save_ollama_job_summary
):
    """Test summarizer flow."""
    raw_fetched_info, summary = "raw", "summary"
    mock_get_raw_offering_data.return_value = raw_fetched_info
    mock_get_ollama_summary.return_value = summary
    summarizer = Summarizer("example.com")
    summarizer.summarize()
    mock_get_raw_offering_data.assert_called_once_with()
    mock_get_ollama_summary.assert_called_once_with(raw_fetched_info)
    mock_save_ollama_job_summary.assert_called_once_with(summary)
