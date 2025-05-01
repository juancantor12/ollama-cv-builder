"""Does."""

import argparse
import sys
from .fetcher import Fetcher

from .summarizer import Summarizer
# from tailor import Tailor
# from generator import Generator


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

	def summarize(self) -> None:
		"""Does."""
		print("Summarizing...")

		summarizer = Summarizer(self.folder_name)
		summarizer.summarize()

	def tailor(self) -> None:
		"""Does."""
		print("Tailoring...")

	# 	tailor = Tailor()
	# 	tailor.tailor()

	def generate(self) -> None:
		"""Does."""
		print("Generating...")

	# 	generator = Generator()
	# 	generator.generate()

	def all(self, url: str) -> None:
		"""Does."""
		self.fetch(url)
		self.summarize()
		self.tailor()
		self.generate()


if __name__ == "__main__":
	CLI = GeneratorCLI()
	SWITCH = {
		"fetch": CLI.fetch,
		"summarize": CLI.summarize,
		"tailor": CLI.tailor,
		"generate": CLI.generate,
		"all": CLI.all,
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
		CLI.all(args.url)
	else:
		actions = args.actions.split("-")
		for action in actions:
			call = SWITCH.get(action)
			if action == "fetch":
				call(args.url)
			else:
				call()
