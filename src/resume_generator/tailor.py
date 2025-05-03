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
						"seed": 42,
						"num_keep": -1,
						"num_predict": 48,
						"top_k": 20,
						"top_p": 0.35,
						"temperature": 0.3,
						"frequency_penalty": 2.0,
						"presence_penalty": 2.0,
						"num_ctx": 8192,
						"stop": ["[Na]", "[NA]", "\n"]
					}
				)
				history += [
					{'role': 'user', 'content': bullet},
					{'role': 'assistant', 'content': response.message.content},
				]
				content = response.message.content if response.message.content != "" else bullet # If no output, keep bullet
				cv_data["experience"][i]["ollama_bullet_list"].append(content)
		return cv_data

	def tailor(self, job_summary) -> None:
		"""Does."""
		cv_data = self.get_cv_json_data()
		tailored_data = self.get_ollama_tailoring(job_summary, cv_data)
		output_path = Utils.get_output_path(self.folder_name, create=False)
		with open(f'{output_path}/tailored_cv.json', 'w', encoding='utf-8') as file:
			json.dump(tailored_data, file, indent=4)
