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
- `context.py` — Builds the system prompt from `data/linkedin.pdf` and `data/summary.txt`, grounding the twin’s answers in professional information.
- `tools.py` — Defines tools for capturing visitor contact details and recording unanswered questions through Pushover.
- `styles.py` — Provides the responsive CSS and JavaScript used by the standalone and portfolio-embedded interfaces.
- `obs.py` — Structured (JSON-per-line) logging helper.
- `ratelimit.py` — In-memory per-session rate limit.

When a visitor submits a question, the application sends the conversation and available tools to an OpenAI model. If the model calls a tool, the application processes it and continues the conversation until a final response is produced.

## Reliability & Operations

The twin is a public endpoint running on a personal OpenAI key and embedded in a
portfolio recruiters open. The following hardening was added so a provider
outage, a bad response, or an abusive client degrades gracefully instead of
showing a stack trace or running up the bill.

**Error handling.** The OpenAI client uses a 30-second timeout with two
automatic retries. `_generate_reply()` runs the tool loop; `chat()` wraps it so
any failure — rate limit, timeout, API error, or an unexpected response shape —
is caught and the visitor sees a calm fallback message (`RateLimitError` gets a
distinct "busy right now" wording), never a traceback. The tool loop is capped
at `MAX_TOOL_ROUNDS` (5); past that it drops the tools and takes one plain text
answer rather than billing an unbounded back-and-forth. `push()` checks the
Pushover HTTP status, uses a 10-second timeout, and returns a success flag
rather than swallowing the response; a failed notification never breaks the
tool call or the conversation. `MODEL_NAME` is required — a missing value stops
startup instead of failing every visitor turn.

**Structured logging.** Every visitor turn emits `request_start` and
`request_end` JSON lines to stdout (captured in the Space logs), correlated by
a short `req_id` and carrying latency, tool-call names, tool rounds, answer
size, and token usage. Failures emit `request_error`; each tool call emits a
`tool_call` line; rate-limited turns emit `rate_limited`. This is what makes
"how is it behaving in production?" answerable.

**Rate limiting.** A per-session sliding-window limit (default 20 turns / 60s,
keyed by Gradio session hash, falling back to client IP) blocks scripted loops.
Blocked turns reply with a "try again in ~N seconds" message and never reach
OpenAI. State is in-memory and per-replica — enough for a single-replica
personal Space; it resets on restart. `tests/test_ratelimit.py` covers the
limiter (`python -m unittest -v`).

Deliberately **out of scope**: streaming, a conversation database, an analytics
dashboard, auth, multi-model support. This is a shipped artifact, not a platform.

**Known gap.** Tool-call and tool-result messages are not carried into the next
turn's model context (only the visitor-facing text is). A visitor who gives
their email and then asks an unrelated question could, in principle, be asked
for it again. The fix is to hold model-side history in a `gr.State` separate
from the displayed chat; not yet done.

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
MODEL_NAME=your_openai_model_id
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_application_token

# optional — rate limit tuning, defaults shown
RATE_LIMIT_MAX=20
RATE_LIMIT_WINDOW_SEC=60
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
├── obs.py              # Structured logging helper
├── ratelimit.py        # Per-session rate limit
├── data/
│   ├── linkedin.pdf    # LinkedIn profile used as grounding context
│   └── summary.txt     # Curated professional summary
├── tests/              # Unit tests (rate limiter)
├── pyproject.toml      # Project metadata and dependencies
├── uv.lock             # Locked dependency versions
├── requirements.txt    # Hugging Face Spaces dependencies
└── README.md           # Project documentation
```

## Purpose

This project demonstrates how an AI assistant can act as an interactive extension of a professional portfolio. Instead of requiring visitors to browse multiple pages, the digital twin lets them ask direct questions about Kervintz’s experience, technical strengths, projects, and approach to engineering.
