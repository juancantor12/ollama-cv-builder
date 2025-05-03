"""Does."""

import argparse
import sys
from .fetcher import Fetcher

from .summarizer import Summarizer
from .tailor import Tailor
from .generator import Generator


class GeneratorCLI:
	"""Does."""

	def __init__(self, url: str = "", folder_name: str = ""):
		self.url = url
		self.folder_name = folder_name

	def fetch(self, url: str) -> None:
		"""Does."""
		print("Fetching...")
		self.url = url
		fetcher = Fetcher(self.url)
		success, folder_name = fetcher.fetch()
		self.folder_name = folder_name
		if not success :
			print(f"Unable to fetch, check the generated file for details: output/{folder_name}/html_free_job_details.txt")
			sys.exit(1)

	def summarize(self) -> str:
		"""Does."""
		print("Summarizing...")
		summarizer = Summarizer(self.folder_name)
		summary = summarizer.summarize()
		return summary

	def tailor(self, summary) -> dict:
		"""Does."""
		print(f"Tailoring...{summary}")
		tailor = Tailor(self.folder_name)
		return tailor.tailor(summary)

	def generate(self, tailored_data) -> None:
		"""Does."""
		print("Generating...")
		generator = Generator(self.folder_name)
		path = generator.generate(tailored_data)
		print(f"Resume generated: {path}")

	def all(self, url: str) -> None:
		"""Does."""
		self.fetch(url)
		summary = self.summarize()
		tailored_data = self.tailor(summary)
		self.generate(tailored_data)


if __name__ == "__main__":
	cli = GeneratorCLI()
	switch = {
		"fetch": cli.fetch,
		"summarize": cli.summarize,
		"tailor": cli.tailor,
		"generate": cli.generate,
		"all": cli.all,
	}
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
	if args.actions == "all" or not args.actions:
		cli.all(args.url)
	else:
		actions = args.actions.split("-")
		for action in actions:
			call = switch.get(action)
			if action == "fetch":
				call(args.url)
			else:
				call()
