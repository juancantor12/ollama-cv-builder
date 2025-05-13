"""Utilities unit testing."""

from unittest.mock import patch
from resume_generator.utils import Utils


def test_url_to_folder_name():
    """Tests that the url to folder name tool works properly."""
    assert "example.com" == Utils.url_to_folder_name("https://example.com")


def test_get_output_path():
    """Tests that the returned output path matches the expected pattern."""
    assert (
        Utils.get_output_path("example.com").as_posix().endswith("/output/example.com")
    )


def test_get_data_path():
    """Tests that the returned data path matches the expected pattern."""
    assert Utils.get_data_path().as_posix().endswith("/data")


@patch("builtins.open")
@patch("resume_generator.utils.Utils.get_output_path")
def save_file_to_output(mock_get_output_path, mock_open):
    """
    Tests that the save_file_to_output tries the write with the correct params.
    This test doesn't test the "create" option
    """
    test_output_path, test_tile_name, test_content = "/output/path", "file.txt", "foo"
    mock_get_output_path.return_value = test_output_path
    mocked_file = mock_open.return_value
    mock_write = mocked_file.__enter__.return_value.write
    Utils.save_file_to_output("example.com", "file.txt", "foo")
    mock_open.assert_called_once_with(
        f"{test_output_path}/{test_tile_name}", "w", encoding="utf-8"
    )
    mock_write.assert_called_once_with(test_content)
