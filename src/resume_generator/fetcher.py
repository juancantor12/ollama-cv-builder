"""Fetchs and cleans an HTML webpage to reduce tokens of the raw page text before model consumption."""
import pathlib
import re
from html import unescape
import requests

class Fetcher():
	"""Initializes the fetch module"""
	def __init__(self, url):
		self.url = url

	def clean_html(self, html: str) -> str:
		"""
		Removes <script>, <style> and <meta> tags completely, replaces other HTML tags with line breaks,
		removes consecutive line breaks and unescape HTML entities
		"""
		html = re.sub(r'<script[\s\S]*?</script>', '', html, flags=re.IGNORECASE)
		html = re.sub(r'<style[\s\S]*?</style>', '', html, flags=re.IGNORECASE)
		html = re.sub(r'<meta[^>]*?>', '', html, flags=re.IGNORECASE)
		html = re.sub(r'<[^>]+>', '\n', html)
		html = re.sub(r'\n+', '\n', html)
		cleaned = unescape(html).strip()
		return cleaned

	def save_clean_html(self, raw_html: str) -> str:
		"""
		Creates the output folder and saves the text cleaned of html tags on it
		"""
		folder_name = ""
		if "//" in self.url:
			split = self.url.split("//")
			folder_name = split[1].replace(".", "-")
		else:
			folder_name = self.url

		path = f"../../output/{folder_name}"
		pathlib.Path(path).mkdir(exist_ok=True)
		with open(f'{path}/html_free_job_details.txt', 'w', encoding='utf-8') as file:
			cleaned = self.clean_html(raw_html)
			file.write(cleaned)
			print(f'HTML free fetched details stored at {path}/html_free_job_details.txt')

		return folder_name

	def fetch(self) -> str:
		"""
		Fetches the html from the provided URL and stores the cleaned text
		"""
		print(f"Fetching {self.url} with 10 seconds timeout")
		response = requests.get(self.url, timeout=10)
		if response.status_code == 200:
			print(response.text)
			raw_html = print(self.url)
			return self.save_clean_html(raw_html)
		return "error"
