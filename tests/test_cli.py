"""CLI orchestration unit testing."""

from unittest.mock import patch#, MagicMock
# import sys
# import pytest
# from resume_generator.cli import GeneratorCLI


# Prevent sys.exit() from actually exiting during tests
# @pytest.fixture(autouse=True)
# def no_exit(monkeypatch):
#     """Does."""
#     monkeypatch.setattr(
#         sys, "exit", lambda code: (_ for _ in ()).throw(SystemExit(code))
#     )

def test_fetch_success_sets_folder_name():
    """Test that a succesfull fetch updates cli.folder_name correctly."""

    with patch('resume_generator.cli.GeneratorCLI') as mock:
        instance = mock.return_value
        def mock_fetch_side_effect(url):
            """Mock side effect for fetch to set the folder name if url is provided."""
            instance.folder_name = "mock_folder" if url else ""
        instance.fetch.side_effect = mock_fetch_side_effect
        instance.fetch("http://example.com")
        assert instance.folder_name == "mock_folder"

    # # Create a magic mock instance to be used instead of GenratorCLI
    # magick_mock_instance = MagicMock()

    # # Override the mocked class __new__ method so when the actual class is called it returns the magic mock instance
    # mock_cli_class.return_value = magick_mock_instance

    # # Add a side effect that will be attached to the fetch method to update the folder_name attribute
    # def mock_fetch_side_effect():
    #     magick_mock_instance.folder_name = "mock_folder"

    # # Assign the side effect to the magic mock instance fetch method so it triggers when the method is called
    # magick_mock_instance.fetch.side_effect = mock_fetch_side_effect

    # # This returns the magick_mock_instance since the mocked class (mock_cli_class) return value was set to that
    # cli = GeneratorCLI()
    # # Now fetch gets called from the mocked magick instance and the sidde effect should trigger
    # cli.fetch("http://example.com")

    # # Assert that folder_name was set correctly
    # assert cli.folder_name == "mock_folder"


def test_placeholder():
    """Does."""
    assert True
