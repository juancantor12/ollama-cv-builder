# Resume Generator (Local, Privacy-First)

[![CI Build](https://img.shields.io/github/actions/workflow/status/juancantor12/ollama-cv-builder/ci.yml?branch=master)](https://github.com/juancantor12/ollama-cv-builder/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

**Resume Generator** is a privacy-focused, fully local Python application that tailors resumes to specific job descriptions by leveraging locally hosted LLMs on low end GPU's (Tested with phi-4:14B, llama3.1:8b and deepseekr1:8b via Ollama on a RTX2060).  
It parses a job description fetched from a URL, summarizes key requirements, and matches them intelligently against your structured professional data to generate a tailored DOCX resume — all without sending any data to the cloud.

---

## Features

- **Fully Local** — No external API calls. All processing happens locally.
- **Privacy-First** — Protects your data and job applications from third-party services.
- **LLM-Driven Tailoring** — Summarizes job descriptions and optimizes your resume using a local LLM.
- **DOCX Resume Output** — Creates professional, ATS-compliant resume files.
- **DevSecOps Friendly** — Includes CI/CD pipelines, linting, testing, and security scanning.

---

## Project Structure
.gitignore
.github/
	└── workflows/
		└── ci.yml 		# CI Pipeline
output/
data/
├── cv_info_template.json
├── cv_info_example.json
src/
└── resume_generator/ 
	├── cli.py 			# Command-line interface 
	├── fetcher.py 		# Fetch and clean job description 
	├── summarizer.py 	# Summarize job text via local LLM  and creates a summary txt file
	├── tailor.py 		# Tailors resume based on the job description file and the JSON resume data
	├── generator.py 	# Builds the final ATS Friendly DOCX file
	├── utils.py 		# Auxiliary functions 
tests/					# Unit testing
Makefile
README.md
requirements.txt
run.sh 					# bash script to run the app


---

## Quick Start

### 1. Clone the repository

```
git clone https://github.com/juancantor12/ollama-cv-builder.git
cd ollama-cv-builder
```
### 2. Install dependencies

```
make install
```

### 3. Lint, format, and test

```
make lint
make format
make test
```

---

## Usage

### Providing Your Resume Data

Before running the application, you must provide your structured resume information.

1. Go to the `data/` folder.
2. Copy `cv_info_template.json` and fill it with your own information.
3. Save it as `cv_info.json`.

> Example files (`cv_info_example.json`) are provided.

After setting up, you can run the CLI directly:
```
cd src
python -m resume_generator.cli fetch https://some-job-url.com
python -m resume_generator.cli summarize
python -m resume_generator.cli tailor
python -m resume_generator.cli generate
```

Or use the provided script:
```
./run.sh "https://some-job-url.com"
```

### Output Structure

Each time you run the pipeline, a **new folder** will be automatically created inside the `output/` directory.

The folder will be named based on:
- The **position title** extracted from the job description
- The **company name** extracted from the job description
- The **timestamp** (formatted as `YYYYMMDD_HHMMSS`)

Example folder name: output/data-scientist-acme-corp-20240418_143500/
Inside each job-specific output folder, you will find:

`summary.txt` | Cleaned and summarized job description
`tailored_cv.json` | Tailored resume data aligned to the job
`final_resume.docx` | Final tailored resume, LLM's can make mistakes so double-check the file


---

## Local LLM Requirements

This app assumes you have:

- Ollama installed and running locally.
- A model of your choice pulled and available.

---

## Contact

- juancantor.all@gmail.com
