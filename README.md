---
title: Kervintz-Digital-Twin
app_file: app.py
sdk: gradio
sdk_version: 6.20.0
---

# Kervintz AI — Digital Twin

An AI-powered digital twin that represents Kervintz Noel’s professional background, technical experience, projects, and engineering approach.

Built with OpenAI and Gradio, the assistant uses curated career information and LinkedIn data to answer questions from recruiters, potential clients, and collaborators. It can capture contact details from interested visitors, record unanswered questions for future improvement, and embed seamlessly into Kervintz’s portfolio website.

## Key Features

- Answers questions about Kervintz’s experience, skills, and projects
- Grounds responses in curated professional and LinkedIn data
- Captures contact information from potential clients and employers
- Records unanswered questions instead of inventing information
- Includes a responsive, portfolio-matched chat interface
- Supports standalone and embedded deployment modes
- Deployable on Hugging Face Spaces

## Built With

- Python
- OpenAI API
- Gradio
- Pypdf
- Pushover API
- Hugging Face Spaces
- uv

## How It Works

- `app.py` — Runs the Gradio chat interface and OpenAI tool-calling loop.
- `context.py` — Builds the system prompt from `linkedin.pdf` and `summary.txt`, grounding the twin’s answers in professional information.
- `tools.py` — Defines tools for capturing visitor contact details and recording unanswered questions through Pushover.
- `styles.py` — Provides the responsive CSS and JavaScript used by the standalone and portfolio-embedded interfaces.

When a visitor submits a question, the application sends the conversation and available tools to an OpenAI model. If the model calls a tool, the application processes it and continues the conversation until a final response is produced.

## Running Locally

### Prerequisites

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- An OpenAI API key
- Pushover credentials

### Installation

Clone the repository:

```bash
git clone https://github.com/kervcodes/Digital-Twin.git
cd Digital-Twin
```

Install the project dependencies:

```bash
uv sync
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_application_token
```

Start the application:

```bash
uv run app.py
```

The application will start locally and display the URL in the terminal.

## Deployment

The application is configured for deployment as a Gradio application on Hugging Face Spaces using the metadata at the top of this README.

It can also be embedded into another website using an iframe. Adding `?embedded=1` to the application URL enables the embedded layout and removes the standalone page styling.

### CI/CD

A GitHub Actions workflow (`.github/workflows/update_space.yml`) deploys the
app automatically on every push to `main`. It checks out the repo, strips
`.github`, commits the remaining files to an orphan `space-deploy` branch,
and force-pushes that branch to the Hugging Face Space
(`Kervcodes/kerv-digital-twin`) as a squashed snapshot — no `gradio deploy`
step is involved. The workflow authenticates with an `HF_TOKEN` repository
secret that must have write access to the Space.

## Project Structure

```text
Digital-Twin/
├── app.py              # Gradio interface and conversation loop
├── context.py          # System prompt and professional context
├── tools.py            # Lead capture and unanswered-question tools
├── styles.py           # Responsive styling and embedded-mode behavior
├── linkedin.pdf        # LinkedIn profile used as grounding context
├── summary.txt         # Curated professional summary
├── pyproject.toml      # Project metadata and dependencies
├── uv.lock             # Locked dependency versions
├── requirements.txt    # Hugging Face Spaces dependencies
└── README.md           # Project documentation
```

## Purpose

This project demonstrates how an AI assistant can act as an interactive extension of a professional portfolio. Instead of requiring visitors to browse multiple pages, the digital twin lets them ask direct questions about Kervintz’s experience, technical strengths, projects, and approach to engineering.
