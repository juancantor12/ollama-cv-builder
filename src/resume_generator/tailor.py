"""Does."""
import json
from ollama import chat
from .utils import Utils

class Tailor:
	"""Does."""

	def __init__(self, folder_name: str = ""):
		self.folder_name = folder_name

	def get_cv_json_data(self) -> str:
		"""Does."""
		data_path = Utils.get_data_path()
		json_data = {}
		with open(f"{data_path}/cv_info.json", "r", encoding="utf-8") as file:
			json_data = json.load(file)
		return json_data

	def get_ollama_tailoring(self, job_summary: str, cv_data: dict) -> str:
		"""Does."""
		history = [
			{"role": "system", "content": "You are a factual rephrasing assistant for an automated resume tailoring system"},
			{"role": "system", "content": "You will receive short career experience inputs and a related job description."},
			{"role": "system", "content": "Your job is to REPHRASE the input experiences to better match the job description"},
			{"role": "system", "content": "You must strictly adhering to the original facts in the resume and no make up data."},
			{"role": "system", "content": (
					"CRITICAL RULES: "
					"- Do NOT invent, infer, or embellish any new achievements. If it is not related, just write [NA]"
					"- ONLY use explicit information present in the original text. "
					"- KEEP each output between 20-30 words. "
					"- USE action verbs. "
					"- MAKE it concise, factual, and structured. "
					"- AVOID repeating the same changes"
					"- DO NOT add summaries, greetings, explanations, or any extra text."
					"- DO NOT write multiple line texts, keep them SINGLE LINE and SHORT"
				)
			},
			{"role": "system", "content": f"Target Job Description: {job_summary} "},
			{"role": "system", "content": "If the text is not STRICTLY related to the job, DONT MODIFY it, just return [NA]"},
			{"role": "system", "content": "remember to keep rephrased texts SHORT AND CONCISE, and SINLGE LINE"},
			{"role": "system", "content": "Begin when the experience text is provided."}
		]
		for i, experience in enumerate(cv_data.get("experience", [])):
			cv_data["experience"][i]["ollama_bullet_list"] = []
			for bullet in experience.get("bullet_list", []):
				response = chat(
					model = 'phi4:latest',
					messages = history + [
						{
							'role': 'system', 
							'content': 'remember, SHORT and FACTUAL rephrasing, if not STRICTLY related to the job, return [NA]'
						},
						{'role': 'user', 'content': bullet},
					],
					options = {
						"seed": 42,						# To replicate inference and testing, can be removed
						"num_keep": -1,					# To not limit the amount of tokens to retain from previous iteration
						"num_predict": 48,				# Aiming for short outputs
						"top_k": 20,					# Give mor freedom for the model to choose
						"top_p": 0.35,					# Pick only really probably tokens, to avoid the model making up stacks
						"temperature": 0.3,				# low temperature to keep the model factual
						"frequency_penalty": 2.0,		# High frequency penalty, tied with no limit on num_keep
						"presence_penalty": 2.0,		# High presence penalty, trying to avoid de model to overfit for the job
						"num_ctx": 8192,				# Max context, can be changed depending on the hardware
						"stop": ["[Na]", "[NA]", "\n"]	# Stop the inference if linebreaks or [NA] are emitted 
					}
				)
				history += [
					{'role': 'user', 'content': bullet},
					{'role': 'assistant', 'content': response.message.content},
				]
				content = response.message.content if response.message.content != "" else bullet # If no output, keep the bullet
				cv_data["experience"][i]["ollama_bullet_list"].append(content)	# Ollama results are stored separately
		return cv_data

	def tailor(self, job_summary) -> dict:
		"""Does."""
		cv_data = self.get_cv_json_data()
		tailored_data = self.get_ollama_tailoring(job_summary, cv_data)
		output_path = Utils.get_output_path(self.folder_name, create=False)
		with open(f'{output_path}/tailored_cv.json', 'w', encoding='utf-8') as file:
			json.dump(tailored_data, file, indent=4)

		return tailored_data
