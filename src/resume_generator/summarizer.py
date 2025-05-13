"""Summarizes a fetched HTML-free job description using a local LLM."""

from ollama import chat
from .utils import Utils


class Summarizer:
    """Summarizes a fetched HTML-free job description using a local LLM."""

    def __init__(self, folder_name: str = ""):
        self.folder_name = folder_name

    def get_raw_offering_data(self) -> str:
        """Takes the html-free fetched job data and returns it if found."""
        output_path = Utils.get_output_path(self.folder_name)
        raw_data = "Raw data was not found"
        with open(
            f"{output_path}/html_free_job_details.txt", "r", encoding="utf-8"
        ) as file:
            raw_data = file.read()
        return raw_data

    def save_ollama_job_summary(self, summary: str) -> bool:
        """
        Saves the ollama generated summary to a text file in output
        """
        return Utils.save_file_to_output(
            folder_name=self.folder_name,
            file_name="ollama_job_summary.txt",
            content=summary,
        )

    def get_ollama_summary(self, raw_info: str) -> str:
        """Performs the inference to summarize the html-free fetched data"""
        response = chat(
            model="phi4:latest",
            messages=[
                {
                    "role": "system",
                    "content": "Your are a meticulous and dedicated assistant",
                },
                {
                    "role": "assistant",
                    "content": """
						The user will provide me raw data from a crawled online job posting,
						he wants me to clear up the HTML and provide a text summary of the job offer
					""",
                },
                {"role": "user", "content": raw_info},
            ],
            options={
                "num_predict": 512,  # Number of max tokens in the output
                "top_k": 10,  # Pick from the top 10 tokens
                "top_p": 0.5,  # Of those 10 pick from the ones that add up to 50% cumulative probability
                "temperature": 0.2,  # Low temp to maintain precission
                "repeat_penalty": 1.5,  # High repeat penalty to prevent the model to repeat requirements
                "mirostat": 0,  # No mirostat
                "num_ctx": 8196,  # Input + output context length
            },
        )
        return response.message.content

    def summarize(self) -> None:
        """Returns the summarized job description."""
        raw_fetched_info = self.get_raw_offering_data()
        summary = self.get_ollama_summary(raw_fetched_info)
        self.save_ollama_job_summary(summary)
