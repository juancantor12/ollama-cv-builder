"""
Modifies a JSON formated cv data based on a job summary to match the requirements without lying.
If the related cv entry is not relevant to the job, it leaves it untouched.
"""

import json
from ollama import chat
from .utils import Utils


class Tailor:
    """
    Modifies a JSON formated cv data based on a job summary to match the requirements without lying.
    If the related cv entry is not relevant to the job, it leaves it untouched.
    """

    def __init__(self, folder_name: str = ""):
        self.folder_name = folder_name

    def get_cv_json_data(self) -> str:
        """Takes the CV data and returns it if it exists."""
        data_path = Utils.get_data_path()
        json_data = {}
        with open(f"{data_path}/cv_info.json", "r", encoding="utf-8") as file:
            json_data = json.load(file)
        return json_data

    def get_job_summary_data(self) -> str:
        """Takes the ollama job summary and returns it if found."""
        output_path = Utils.get_output_path(self.folder_name)
        with open(
            f"{output_path}/ollama_job_summary.txt", "r", encoding="utf-8"
        ) as file:
            return file.read()

    def save_ollama_tailored_data(self, tailored_data: dict) -> bool:
        """
        Saves the ollama tailored_data to a json file in output
        """
        return Utils.save_file_to_output(
            folder_name=self.folder_name,
            file_name="tailored_cv.json",
            content=json.dumps(tailored_data, indent=4),
        )

    def get_ollama_tailoring(self, job_summary: str, cv_data: dict) -> str:
        """Perform iterative inference on each job experience bullet list to rephrase it based on the job summary."""
        history = [
            {
                "role": "system",
                "content": (
                    "You are a factual rephrasing assistant for an automated resume tailoring system"
                    "You will receive short career experience inputs and a related job description."
                    "Your job is to REPHRASE the input experiences to better match the job description"
                    "You must strictly adhering to the original facts in the resume and no make up experience."
                    "CRITICAL RULES: "
                    "- Do NOT invent, infer, or embellish any new achievements. If the entry is not related, write [NA]"
                    "- ONLY use explicit information present in the original experience. "
                    "- KEEP each output between 15-30 words. "
                    "- USE action verbs. "
                    "- MAKE it concise, factual, and structured. "
                    "- AVOID repeating the same changes on different entries"
                    "- DO NOT add summaries, greetings, explanations, or any extra text."
                    "- DO NOT write multiple line texts, keep them SINGLE LINE and SHORT"
                ),
            },
            {"role": "system", "content": f"Target Job Description: {job_summary} "},
            {
                "role": "system",
                "content": (
                    "If the text is not STRICTLY related to the job, DONT MODIFY it, just return [NA]"
                    "remember to keep rephrased texts SHORT, CONCISE and SINLGE LINE"
                ),
            },
        ]
        for i, experience in enumerate(cv_data.get("experience", [])):
            cv_data["experience"][i]["ollama_bullet_list"] = []
            instruction = "The next {n} entries belong to a job as a {position} at {company} from {duration}".format(  # pylint: disable=consider-using-f-string
                n=len(experience.get("bullet_list", [])),
                position=experience.get("position", ""),
                company=experience.get("company", ""),
                duration=experience.get("duration", ""),
            )
            history += [
                {
                    "role": "system",
                    "content": (
                        f"{instruction}"
                        "Remember, SHORT and FACTUAL rephrasing, if not STRICTLY related to the job, return [NA]"
                        "DONT REPEAT information already covered in previous entries"
                        "If the requirements were already covered on previous entries just return [NA]"
                        "The user will start providing this job entries now:."
                    ),
                }
            ]
            for bullet in experience.get("bullet_list", []):
                response = chat(
                    model="phi4:latest",
                    messages=history
                    + [
                        {"role": "user", "content": bullet},
                    ],
                    options={
                        "seed": 42,  # To replicate inference and testing, can be removed
                        "num_keep": -1,  # No limit on amount of tokens to retain from previous iteration
                        "num_predict": 48,  # Aiming for short outputs
                        "top_k": 20,  # Give mor freedom for the model to choose
                        "top_p": 0.35,  # Pick only probably tokens, to avoid the model making up stacks
                        "temperature": 0.3,  # low temperature to keep the model factual
                        "frequency_penalty": 2.0,  # High frequency penalty, tied with no limit on num_keep
                        "presence_penalty": 2.0,  # High presence penalty, to avoid de model to overfit for the job
                        "num_ctx": 8192,  # Max context, can be changed depending on the hardware
                        "stop": [
                            "[Na]",
                            "[NA]",
                            "\n",
                        ],  # Stop the inference if linebreaks or [NA] are emitted
                    },
                )
                history += [
                    {
                        "role": "system",
                        "content": (
                            f"The user provided this entry: {bullet}"
                            f"You rephrased it to: {response.message.content}"
                            "You should not repeat this same rephrasing on future entries"
                        ),
                    }
                ]
                cv_data["experience"][i]["ollama_bullet_list"].append(
                    response.message.content
                )  # Ollama results are stored separately
        return cv_data

    def tailor(self) -> None:
        """Entry point for the tailor module, stores and returns the tailored data."""
        cv_data = self.get_cv_json_data()
        job_summary = self.get_job_summary_data()
        tailored_data = self.get_ollama_tailoring(job_summary, cv_data)
        self.save_ollama_tailored_data(tailored_data)
