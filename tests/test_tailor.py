"""
Tests for the tailor submodule.
The following functions are not covered because they are too trivial:
    - save_ollama_tailored_data
"""

import json
from unittest.mock import patch
from resume_generator.tailor import Tailor


@patch("builtins.open")
@patch("resume_generator.utils.Utils.get_data_path")
def test_get_cv_json_data(mock_get_data_path, mock_open):
    """Test succesfully opening the file."""
    mock_get_data_path.return_value = "/data/path"
    test_data = '{"file": "data"}'
    mocked_file = mock_open.return_value
    mock_read = (
        mocked_file.__enter__.return_value.read
    )  # __enter__ because of "with" opening
    mock_read.return_value = test_data
    tailor = Tailor("example.com")
    json_data = tailor.get_cv_json_data()
    mock_open.assert_called_once_with("/data/path/cv_info.json", "r", encoding="utf-8")
    assert json_data == json.loads(test_data)


@patch("builtins.open")
@patch("resume_generator.utils.Utils.get_output_path")
def test_get_job_summary_data(mock_get_output_path, mock_open):
    """Test succesfully opening the file."""
    mock_get_output_path.return_value = "/out/path"
    test_data = "summary data"
    folder_name = "example.com"
    mocked_file = mock_open.return_value
    mock_read = (
        mocked_file.__enter__.return_value.read
    )  # __enter__ because of "with" opening
    mock_read.return_value = test_data
    tailor = Tailor(folder_name)
    summary_data = tailor.get_job_summary_data()
    mock_get_output_path.assert_called_once_with(folder_name)
    mock_open.assert_called_once_with(
        "/out/path/ollama_job_summary.txt", "r", encoding="utf-8"
    )
    assert summary_data == test_data


def test_get_ollama_tailoring():  # TODO
    """Test the entire inference flow mocking ollama chat calls."""
    assert True


@patch("resume_generator.tailor.Tailor.save_ollama_tailored_data")
@patch("resume_generator.tailor.Tailor.get_ollama_tailoring")
@patch("resume_generator.tailor.Tailor.get_job_summary_data")
@patch("resume_generator.tailor.Tailor.get_cv_json_data")
def test_summarize(
    mock_get_cv_json_data,
    mock_get_job_summary_data,
    mock_get_ollama_tailoring,
    mock_save_ollama_tailored_data,
):
    """Test tailor flow."""
    cv_data, job_summary, tailored_data = {"a": 1}, "summary", {"a": 2}
    mock_get_cv_json_data.return_value = cv_data
    mock_get_job_summary_data.return_value = job_summary
    mock_get_ollama_tailoring.return_value = tailored_data
    tailor = Tailor("example.com")
    tailor.tailor()
    mock_get_cv_json_data.assert_called_once_with()
    mock_get_job_summary_data.assert_called_once_with()
    mock_get_ollama_tailoring.assert_called_once_with(job_summary, cv_data)
    mock_save_ollama_tailored_data.assert_called_once_with(tailored_data)
