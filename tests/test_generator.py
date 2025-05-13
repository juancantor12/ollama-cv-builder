"""Tests for the docx generator script."""

from unittest.mock import patch, call
from resume_generator.generator import Generator


@patch("resume_generator.docx_factory.DocxFactory.add_text")
def test_write_profile(mock_add_text):
    """
    Tests correc profile information injection into the document.
    The main objective of this test is to showcase how unnecesary some tests are
    when chasing high percentual coverage.
    """
    generator = Generator("example.com")
    generator.write_profile(
        {
            "name": "Jhon Doe",
            "title": "CEO of Mars",
            "location": "Mars",
            "email": "jhon@mars.com",
        }
    )
    mock_add_text.assert_has_calls(
        [
            call(
                text="Jhon Doe", bold=True, uppercase=True, font_size=18, centered=True
            ),
            call(
                text="CEO of Mars | Mars | jhon@mars.com", font_size=12, centered=True
            ),
        ]
    )
    assert mock_add_text.call_count == 2


@patch("resume_generator.docx_factory.DocxFactory.add_line_breaks")
@patch("resume_generator.docx_factory.DocxFactory.bulleted")
@patch("resume_generator.docx_factory.DocxFactory.add_horizontal_line")
@patch("resume_generator.docx_factory.DocxFactory.add_text")
def test_write_education(
    mock_add_text, mock_add_horizontal_line, mock_bulleted, mock_add_line_breaks
):
    """Tests that education writting is called the correct amount of times."""
    bullets = ["a", "b", "c"]
    test_educations = [
        {
            "degree": "Degree #1",
            "collegue": "Cool Collgeue",
            "location": "Somewhere",
            "date": "The other day",
            "bullet_list": bullets,
        },
        {
            "degree": "Doctor",
            "collegue": "Prestigious Collgeue",
            "location": "Here",
            "date": "Last week",
            "bullet_list": bullets,
        },
    ]
    generator = Generator("example.com")
    generator.write_education(test_educations)
    assert mock_add_text.call_count == 1 + (2 * len(test_educations)) + (
        len(test_educations) * len(bullets)
    )
    assert mock_add_horizontal_line.call_count == 1
    assert mock_bulleted.call_count == len(test_educations) * len(bullets)
    assert mock_add_line_breaks.call_count == len(test_educations)


@patch("resume_generator.docx_factory.DocxFactory.add_line_breaks")
@patch("resume_generator.docx_factory.DocxFactory.bulleted")
@patch("resume_generator.docx_factory.DocxFactory.add_horizontal_line")
@patch("resume_generator.docx_factory.DocxFactory.add_text")
def test_write_experience(
    mock_add_text, mock_add_horizontal_line, mock_bulleted, mock_add_line_breaks
):
    """Tests that experiences writting is called the correct amount of times."""
    bullets = ["a", "b", "c"]
    skills = ["x", "y", "z"]
    test_experiences = [
        {
            "position": "CEO #1",
            "company": "Bad Company",
            "location": "Somewhere",
            "contract_type": "Blood pact",
            "duration": "Forever",
            "ollama_bullet_list": bullets,
            "skills": skills,
        },
        {
            "position": "Cleaning lady",
            "company": "My own house",
            "location": "Here",
            "contract_type": "Voluntary",
            "duration": "Once a month",
            "ollama_bullet_list": bullets,
            "skills": skills,
        },
    ]
    generator = Generator("example.com")
    generator.write_experience(test_experiences)
    mock_add_horizontal_line.assert_called_once_with()
    assert mock_add_text.call_count == 1 + (3 * len(test_experiences)) + (
        len(test_experiences) * (len(bullets))
    )
    assert mock_bulleted.call_count == len(test_experiences) * len(bullets)
    assert mock_add_line_breaks.call_count == 2 * len(test_experiences)


@patch("resume_generator.docx_factory.DocxFactory.add_line_breaks")
@patch("resume_generator.docx_factory.DocxFactory.add_horizontal_line")
@patch("resume_generator.docx_factory.DocxFactory.add_text")
def test_write_others(mock_add_text, mock_add_horizontal_line, mock_add_line_breaks):
    """Tests that "others" writting is called the correct amount of times."""
    test_sections = ["a", "b"]
    entries = [
        {"title": "t1", "description": "d1"},
        {"title": "t2", "description": "d2"},
    ]
    test_others = {"a": entries, "b": entries}
    generator = Generator("example.com")
    generator.write_others(test_others, test_sections)
    assert mock_add_text.call_count == len(test_sections) + (
        2 * len(test_sections) * len(entries)
    )
    assert mock_add_line_breaks.call_count == 1 + len(test_sections)
    assert mock_add_horizontal_line.call_count == len(test_sections)


@patch("resume_generator.docx_factory.DocxFactory.save_document")
@patch("resume_generator.utils.Utils.get_output_path")
@patch("resume_generator.generator.Generator.write_others")
@patch("resume_generator.generator.Generator.write_experience")
@patch("resume_generator.generator.Generator.write_education")
@patch("resume_generator.generator.Generator.write_profile")
@patch("resume_generator.generator.Generator.get_tailored_data_file")
def test_generate(  # pylint: disable=too-many-arguments
    mock_get_tailored_data_file,
    mock_write_profile,
    mock_write_education,
    mock_write_experience,
    mock_write_others,
    mock_get_output_path,
    mock_save_document,
):
    """Test the correct execution of Generators methods when calling .generate."""
    test_folder_name = "example.com"
    test_data = {"profile_info": 1, "education": 2, "experience": 3}
    sections = ["continuous_learning", "personal_projects", "personal_development"]
    test_path = "/path"
    mock_get_tailored_data_file.return_value = test_data
    mock_get_output_path.return_value = test_path
    generator = Generator(test_folder_name)
    returned_path = generator.generate()
    mock_get_tailored_data_file.assert_called_once_with()
    mock_write_profile.assert_called_once_with(1)
    mock_write_education.assert_called_once_with(2)
    mock_write_experience.assert_called_once_with(3)
    mock_write_others.assert_called_once_with(test_data, sections)
    mock_get_output_path.assert_called_once_with(test_folder_name)
    mock_save_document.assert_called_once_with(test_path)
    assert returned_path == test_path
