"""Does."""
import sys
from fetcher import Fetcher
# from summarizer import Summarizer
# from tailor import Tailor
# from generator import Generator

class GeneratorCLI:
	"""Does."""
	def __init__(self, folder_name: str=""):
		self.folder_name = folder_name

	def fetch(self, url: str) -> None:
		"""Does."""
		fetcher = Fetcher(url)
		self.folder_name = fetcher.fetch()
		if self.folder_name == "error":
			print(f"Unable to fetch {url}")
			sys.exit(1)

	# def summarize(self) -> None:
	# 	"""Does."""
	# 	summarizer = Summarizer()
	# 	summarizer.summarize()

	# def tailor(self) -> None:
	# 	"""Does."""
	# 	tailor = Tailor()
	# 	tailor.tailor()

	# def generator(self) -> None:
	# 	"""Does."""
	# 	generator = Generator()
	# 	generator.generate()

	def all(self, url: str) -> None:
		"""Does."""
		self.fetch(url)
		# self.summarize()
		# self.tailor()
		# self.generator()

if __name__ == "__main__":
	CLI = GeneratorCLI()
	SWITCH = {
		"fetch": CLI.fetch,
		# "summarize": CLI.summarize,
		# "tailor": CLI.tailor,
		# "generate": CLI.generate,
		"all": CLI.all
	}

	call = SWITCH.get(sys.argv[1], "all")
	if sys.argv[1] == "fetch" or sys.argv[1] == "all":
		call(sys.argv[2])
	else:
		call()
