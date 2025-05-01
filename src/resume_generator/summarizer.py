"""Does."""
from ollama import chat
from .utils import Utils

class Summarizer:
	"""Does."""

	def __init__(self, folder_name: str = ""):
		self.folder_name = folder_name

	def get_raw_offering_data(self) -> str:
		"""Does."""
		output_path = Utils.get_output_path(self.folder_name, create=False)
		raw_data = "Raw data was not found"
		with open(f"{output_path}/html_free_job_details.txt", "r", encoding="utf-8") as file:
			raw_data = file.read()
		return raw_data

	def get_ollama_summary(self, raw_info: str) -> str:
		"""Does."""
		response = chat(
			model = 'phi4:latest',
			messages = [
				{'role': 'system', 'content': "Your are a meticulous and dedicated assistant"},
				{
					"role": "assistant",
					"content": 
					"""
						The user will provide me raw data from a crawled online job posting,
						he wants me to clear it up on a more readable format along a tex-based description of the job
					"""
				},
				{'role': 'user', 'content': raw_info }
			],
			options = {
				"num_predict": 512,		# Number of max tokens in the output
				"top_k": 10,			# Pick from the top 10 tokens
				"top_p": 0.5,			# Of those 10 pick from the ones that add up to 50% cumulative probability
				"temperature": 0.2,		# Low temp to maintain precission
				"repeat_penalty": 1.5,	# High repeat penalty to prevent the model to repeat requirements
				"mirostat": 0,			# No mirostat
				"num_ctx": 8196,		# Input + output context length
			}
		)
		return response.message.content

	def summarize(self) -> str:
		"""Does."""
		raw_fetched_info = self.get_raw_offering_data()
		summary = self.get_ollama_summary(raw_fetched_info)
		return summary
