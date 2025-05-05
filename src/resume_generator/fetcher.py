"""Fetchs and cleans an HTML webpage to reduce tokens of the raw page text before model consumption."""
import re
from html import unescape
import requests
from .utils import Utils

class Fetcher:
	"""Fetchs and cleans an HTML webpage to reduce tokens of the raw page text before model consumption."""

	def __init__(self, url):
		self.url = url

	def clean_html(self, html: str) -> str:
		"""
		Removes <script>, <style> and <meta> tags completely, replaces other HTML tags with line breaks,
		removes consecutive line breaks and unescape HTML entities
		"""
		html = re.sub(r"<script[\s\S]*?</script>", "", html, flags=re.IGNORECASE)
		html = re.sub(r"<style[\s\S]*?</style>", "", html, flags=re.IGNORECASE)
		html = re.sub(r"<meta[^>]*?>", "", html, flags=re.IGNORECASE)
		html = re.sub(r"<[^>]+>", "\n", html)
		html = re.sub(r"\n+", "\n", html)
		cleaned = unescape(html).strip()
		return cleaned

	def save_clean_html(self, raw_html: str) -> str:
		"""
		Creates the output folder and saves the text cleaned of html tags on it
		"""
		folder_name = Utils.url_to_folder_name(self.url)
		output_path = Utils.get_output_path(folder_name, create=True)
		with open(f"{output_path}/html_free_job_details.txt", "a", encoding="utf-8") as file:
			cleaned = self.clean_html(raw_html)
			file.write(cleaned)
			print(
				f"HTML free fetched details stored at {output_path}/html_free_job_details.txt"
			)

		return folder_name

	def fetch(self) -> (bool, str):
		"""
		Fetches the html from the provided URL and stores the cleaned text
		"""
		print(f"Fetching {self.url} with 10 seconds timeout")
		response = requests.get(self.url, timeout=10)
		if response.status_code == 200:
			return (True, self.save_clean_html(response.text))
		folder_name = self.save_clean_html(
			f"""
			Unable to fetch, the server has denied the request.
			fill this job summary manually and rerun providing same URL but without fetching and summarizing
			[.\\run.sh or .\\run.ps1] -url {self.url} -actions tailor-generate
			providing the same url will make the application run using this file, delete this message
			and fill the job details manually from the page.
			"""
		)
		return (False, folder_name)
