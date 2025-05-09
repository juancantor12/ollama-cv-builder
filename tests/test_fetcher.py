"""Does."""

from unittest.mock import patch, MagicMock
from resume_generator.fetcher import Fetcher


def test_clean_html():
    """
    Test that this function removes all script, style and meta tags entirely.
    It also should remove all html tags and collapse all line breaks into a single one
    Lastly, it should unescape HTML entities and strip trailing whitespaces.
    """
    raw_html = """
    <script>alert(1);</script>
    <style>
        p {color:blue;}
    </style>
    <meta content="text/html; charset=UTF-8">
    <title>12/hr Job offer</title>
    <body>
        <h1>We need an unicorn-god-wizzard quantum galactic engineer overlord</h1>
        Requirements:
        <ul>
            <li>Able to Code a Turing Machine that Determines Whether an Algorithm Halts</li>
            <li>Capable of Writing a Gödel Proof that Shows All True Statements Can Be Proven, in assembly</li>
            <li>Fluent in Binary, Hexadecimal is a plus</li>
        </ul>
    </body>
    """
    expected_html = """12/hr Job offer\n    \n        \nWe need an unicorn-god-wizzard quantum galactic engineer overlord\n        Requirements:\n        \n            \nAble to Code a Turing Machine that Determines Whether an Algorithm Halts\n            \nCapable of Writing a Gödel Proof that Shows All True Statements Can Be Proven, in assembly\n            \nFluent in Binary, Hexadecimal is a plus"""  # pylint: disable=line-too-long
    fetcher = Fetcher("https://example.com")
    cleaned = fetcher.clean_html(raw_html)
    assert cleaned == expected_html


@patch("resume_generator.utils.Utils.save_file_to_output")
def test_save_html_job_details(mock_save_file_to_output):
    """Tests that save_html_job_details gets called with the appropiate parameters."""
    fetcher = Fetcher("https://example.com")
    fetcher.save_html_job_details("<tag>raw_html</tag>")
    assert mock_save_file_to_output.called_once_with(
        folder_name="example.com",
        file_name="html_free_job_details.txt",
        content="raw_html",
        create=True,
    )


@patch("requests.get")
@patch("resume_generator.fetcher.Fetcher.save_html_job_details")
def test_fetch_success(mock_save_html_job_details, mock_get):
    """
    Tests that after a succesfull requests.get call, the method
    attempts to save and return True.
    """
    magic_mock_response = MagicMock()
    magic_mock_response.status_code = 200
    magic_mock_response.text = "<html>Example job offer</html>"
    mock_get.return_value = magic_mock_response
    fetcher = Fetcher("https://example.com")
    okey = fetcher.fetch()
    assert mock_save_html_job_details.called_once_with("<html>Example job offer</html>")
    assert okey


@patch("requests.get")
@patch("resume_generator.fetcher.Fetcher.save_html_job_details")
def test_fetch_fail(mock_save_html_job_details, mock_get):
    """
    Tests that after a unsuccesfull requests.get call, the method
    attempts to save a warning text and returns False.
    """
    magic_mock_response = MagicMock()
    magic_mock_response.status_code = 403
    mock_get.return_value = magic_mock_response
    fetcher = Fetcher("https://selfish-jobboard.com")
    okeynt = not fetcher.fetch()
    assert mock_save_html_job_details.called_once_with(
        f"""
        Unable to fetch, the server has denied the request.
        fill this job summary manually and rerun providing same URL but without fetching and summarizing
        [.\\run.sh or .\\run.ps1] -url {fetcher.url} -actions tailor-generate
        providing the same url will make the application run using this file, delete this message
        and fill the job details manually from the page.
        """
    )
    assert okeynt
