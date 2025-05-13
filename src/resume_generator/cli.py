"""Entry point for the application."""

import argparse
import sys
from .fetcher import Fetcher
from .summarizer import Summarizer
from .tailor import Tailor
from .generator import Generator
from .utils import Utils


class GeneratorCLI:
    """Entry point for the application."""

    def __init__(self, url: str = ""):
        self.url = url
        self.folder_name = Utils.url_to_folder_name(url)

    def fetch(self) -> None:
        """
        Wrapper for the Fetch module call
        if the fetch fails, exit the system with error code
        """
        print("Fetching...")
        fetcher = Fetcher(self.url)
        if not fetcher.fetch():
            print(
                f"Unable to fetch, details at output/{self.folder_name}/html_free_job_details.txt"
            )
            sys.exit(1)

    def summarize(self) -> str:
        """
        Wrapper for the Summarizer module call
        """
        print("Summarizing...")
        summarizer = Summarizer(self.folder_name)
        summarizer.summarize()

    def tailor(self) -> dict:
        """
        Wrapper for the Tailor module call
        """
        print("Tailoring...")
        tailor = Tailor(self.folder_name)
        tailor.tailor()

    def generate(self) -> None:
        """
        Wrapper for the Generator module call
        prints the path to the generated docx resume
        """
        print("Generating...")
        generator = Generator(self.folder_name)
        path = generator.generate()
        print(f"Resume generated: {path}")

    def all(self) -> None:
        """Performs all of the operations in order."""
        self.fetch()
        self.summarize()
        self.tailor()
        self.generate()


if __name__ == "__main__":
    valid_actions = ["fetch", "summarize", "tailor", "generate", "all"]
    parser = argparse.ArgumentParser(description="AI CV generator")
    parser.add_argument(
        "--url",
        help="URL to fetch data from, if the getch fail, fill the generated file manually and rerun skipping fetch",
        required=True,
    )
    parser.add_argument(
        "--actions",
        help=f'Actions to perform, if empty all actions will be executed, valid actions = {", ".join(valid_actions)}',
        required=False,
    )
    args = parser.parse_args()
    cli = GeneratorCLI(args.url)
    switch = {
        "fetch": cli.fetch,
        "summarize": cli.summarize,
        "tailor": cli.tailor,
        "generate": cli.generate,
        "all": cli.all,
    }
    if args.actions == "all" or not args.actions:
        cli.all()
    else:
        actions = args.actions.split("-")
        for action in actions:
            call = switch.get(action)
            call()
