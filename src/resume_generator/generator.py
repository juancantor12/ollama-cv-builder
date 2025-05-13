"""Generates an ATS friendly docx file based on the tailored cv json data."""

import json
from .utils import Utils
from .docx_factory import DocxFactory


class Generator:
    """Generates an ATS friendly docx file based on the tailored cv json data."""

    def __init__(self, folder_name: str = ""):
        self.folder_name = folder_name
        self.docx_factory = DocxFactory()

    def get_tailored_data_file(self) -> dict:
        """Takes the tailored CV data and returns it if it exists."""
        output_path = Utils.get_output_path(self.folder_name)
        with open(f"{output_path}/tailored_cv.json", "r", encoding="utf-8") as file:
            return json.load(file)

    def write_profile(self, profile: dict) -> None:
        """Writes the profile info into the document."""
        self.docx_factory.add_text(
            text=profile["name"], bold=True, uppercase=True, font_size=18, centered=True
        )
        info_line = f'{profile["title"]} | {profile["location"]} | {profile["email"]}'
        self.docx_factory.add_text(text=info_line, font_size=12, centered=True)

    def write_education(self, educations: list) -> None:
        """Writes the education info into the document."""
        self.docx_factory.add_text(
            text="EDUCATION", bold=True, uppercase=True, font_size=13
        )
        self.docx_factory.add_horizontal_line()
        for education in educations:
            header = f"{education['degree']} – {education['collegue'].upper()}"
            self.docx_factory.add_text(text=header, bold=True)
            info = f'{education["location"]}, {education["date"]}.'
            self.docx_factory.add_text(text=info, italic=True)

            for bullet in education.get("bullet_list", []):
                self.docx_factory.add_text(
                    text=self.docx_factory.bulleted(bullet), font_size=10
                )

            self.docx_factory.add_line_breaks(1)

    def write_experience(self, experiences: list) -> None:
        """Writes the experience info into the document."""
        self.docx_factory.add_text(
            text="EXPERIENCE", bold=True, uppercase=True, font_size=13
        )
        self.docx_factory.add_horizontal_line()
        for experience in experiences:
            header = f"{experience['position']} – {experience['company'].upper()}"
            self.docx_factory.add_text(text=header, bold=True)
            info = f'{experience["location"]}, {experience["contract_type"]}, {experience["duration"]}.'
            self.docx_factory.add_text(text=info, italic=True)

            for i, bullet in enumerate(experience.get("ollama_bullet_list", [])):
                self.docx_factory.add_text(
                    text=self.docx_factory.bulleted(
                        bullet if bullet != "" else experience["bullet_list"][i]
                    ),
                    font_size=10,
                )

            self.docx_factory.add_line_breaks(1)
            if "skills" in experience:
                self.docx_factory.add_text(
                    text=f"Skills: {' • '.join(experience['skills'])}", italic=True
                )

            self.docx_factory.add_line_breaks(1)

    def write_others(self, data: dict, sections: list) -> None:
        """Writes additional info into the document."""
        self.docx_factory.add_line_breaks(2)
        for section in sections:
            self.docx_factory.add_text(
                text=section, bold=True, uppercase=True, font_size=13
            )
            self.docx_factory.add_horizontal_line()
            for entry in data.get(section, []):
                self.docx_factory.add_text(text=entry["title"], italic=True, bold=True)
                self.docx_factory.add_text(text=entry["description"], font_size=10)
            self.docx_factory.add_line_breaks(1)

    def generate(self) -> str:
        """Generates the docx file based on the given data and store it on the output folder."""
        data = self.get_tailored_data_file()
        self.write_profile(data["profile_info"])
        self.write_education(data["education"])
        self.write_experience(data["experience"])
        self.write_others(
            data, ["continuous_learning", "personal_projects", "personal_development"]
        )
        output_path = Utils.get_output_path(self.folder_name)
        self.docx_factory.save_document(output_path)
        return output_path
