# Resume Generator (Local, Privacy-First)

[![CI Build](https://github.com/juancantor12/ollama-cv-builder/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/juancantor12/ollama-cv-builder/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

**Resume Generator** is a privacy-focused, fully local Python application that tailors resumes to specific job descriptions by leveraging locally hosted LLMs on low end GPU's (Tested with phi-4:14B, llama3.1:8b and deepseekr1:8b via Ollama on a RTX2060).  
It parses a job description fetched from a URL, summarizes key requirements, and matches them intelligently against your structured professional data to generate a tailored DOCX resume — all without sending any data to the cloud.

---

## Features

- **Fully Local** — No external API calls. All processing happens locally.
- **Privacy-First** — Protects your data and job applications from third-party services.
- **LLM-Driven Tailoring** — Summarizes job descriptions and optimizes your resume using a local LLM.
- **DOCX Resume Output** — Creates professional, ATS-friendly resume documents.
- **DevSecOps Friendly** — Includes CI/CD pipelines, formating, linting, testing, and security scanning.

---


## Setup

### 1. Clone the repository

```
git clone https://github.com/juancantor12/ollama-cv-builder.git
cd ollama-cv-builder
```
### 2. Seup environment, either with run.sh on lunux or run.ps1 on windows  
For linux soyboys it's advised to setup a virtual environment and activate it first.  

```
./run.sh -setup
```
or well
```
./run.ps1 -setup	# For windows dev gigachads, no venv
```

## You can optionally run each steps by your own

```
./run.sh -install
```
or
```
./run.ps1 -test
```

This linux bash script uses a make file underneath, steps could also be made using make directly.
Both windows and linux run files provide a -help option for more details.

---

## Usage

### Providing Your Resume Data

Before running the application, you must provide your structured resume information.

1. Go to the `data/` folder.
2. Copy `cv_info_template.json` and fill it with your own information.
3. Save it as `cv_info.json`.

> Example files (`cv_info_example.json`) are provided.

After setting up, you can use one of the provided scripts for linux or windows respectively:

```
./run.sh -url https://example.com -actions fetch-summarize
```
```
.\run.ps1 -url https://example.com -actions tailor-generate
```

Or run the CLI directly:
```
python -m src.resume_generator.cli --url https://example.com --actions fetch-summarize-tailor-generate
```

### Output Structure

Each time you run the pipeline, a **new folder** will be automatically created inside the `output/` directory.

The folder will be named based on the provided url  

Inside each job-specific output folder, you will find:

`html_free_job_details.txt` | Fetched job details stripped of most html tags  

`ollama_job_summary.txt` | Cleaned and summarized job description  

`tailored_cv.json` | Tailored (experience) resume data aligned to the job in json format  

`generated_resume.docx` | Final tailored resume, LLM's can make mistakes so double-check the file  

The tailoring process adds a "ollama_bullet_list" sections with the llm suggestions, the generator will use these but all the original entries will be preserved on this file.

---

## Local LLM Requirements

This app assumes you have:

- Ollama installed and running locally.
- A model of your choice pulled and available.

---

### Roadmap & changelog

Im planning on adding an interface to generate the original cv json data from a provided docx or pdf file, and to have a user interface wizzard for the whole process, allowing the user to make changes along the way.  
I won't be working on this in the near future tough  

I disabled pip-audit on the github workflow CI because it takes a lot of time but it still runs locally when calling any of the run scripts with the -audit flag

---

## Contact

- juancantor.all@gmail.com
