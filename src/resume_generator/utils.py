"""Utilities for the CV builder."""

import pathlib
import re


class Utils:
    """Utilities for the CV builder."""

    def __init__(self, folder_name):
        self.folder_name = folder_name

    @staticmethod
    def url_to_folder_name(url: str) -> str:
        """Sanitizes an url to be used as a folder name"""
        sanitized = (
            url.replace("http://", "").replace("https://", "").replace("//", "_")
        )
        reserved_chars = r'[\\/*?:"<>|]'
        sanitized = re.sub(reserved_chars, "_", sanitized)
        sanitized = sanitized.strip()
        return sanitized

    @staticmethod
    def get_output_path(folder_name: str, create: bool = False) -> str:
        """Returns the absolute output path for a given folder name."""
        path = f"output/{folder_name}"
        root_path = pathlib.Path(__file__).resolve().parents[2]
        output_path = root_path / path
        if create:
            pathlib.Path(output_path).mkdir(exist_ok=True)
        return output_path

    @staticmethod
    def get_data_path() -> str:
        """Returns the absolute data path."""
        path = "data"
        root_path = pathlib.Path(__file__).resolve().parents[2]
        data_path = root_path / path
        return data_path

    @staticmethod
    def save_file_to_output(
        folder_name: str, file_name: str, content: str, create: bool = False
    ) -> bool:
        """
        Saves a file to a subfolder in /output, if the folder doesnt exists it is created
        """
        output_path = Utils.get_output_path(folder_name, create=create)
        with open(f"{output_path}/{file_name}", "w", encoding="utf-8") as file:
            file.write(content)
            print(f"Saving to output/{file_name}")

        return True
