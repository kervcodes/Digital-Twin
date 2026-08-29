from openai import OpenAI, APIError, APITimeoutError, RateLimitError
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from obs import log_event, new_request_id
from styles import CSS, EXAMPLES, FOCUS_JS, EMBED_JS
from dotenv import load_dotenv
import gradio as gr
import ratelimit
import spaces
import time
import os

load_dotenv(override=True)

MODEL_NAME = os.getenv("MODEL_NAME")
if not MODEL_NAME:
    # Fail loudly at startup rather than turning every visitor turn into a
    # 400 from OpenAI. Set MODEL_NAME in .env locally or in the Space secrets;
    # it must be a current OpenAI model id.
    raise RuntimeError("MODEL_NAME is not set — refusing to start.")

# Bound every model call so a hung connection can't leave a visitor staring at
# the typing indicator forever.
openai = OpenAI(timeout=30.0, max_retries=2)

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]

# Shown to the visitor whenever the model round-trip fails. Deliberately vague —
# a recruiter should see a calm message, not a stack trace or a provider error.
ERROR_REPLY = (
    "Sorry — I ran into a problem answering that. Please try again in a moment."
)
BUSY_REPLY = (
    "I'm getting a lot of traffic right now and couldn't get to that one. "
    "Please try again shortly."
)

# A cooperating model resolves its tools in one or two rounds. More than this
# is a loop — stop feeding it and force a text answer rather than billing for
# an unbounded back-and-forth.
MAX_TOOL_ROUNDS = 5

BRAND_NAME = "Kervintz AI"
HERO_GREETING = "Hi, I'm Kervintz's AI digital twin"
HERO_HEADLINE = "What would you like to know?"
HERO_SUBTEXT = (
    "Ask about my professional background, technical experience, "
    "projects, or engineering approach."
)
INPUT_PLACEHOLDER = "Ask me anything about Kervintz's professional work"


# Generation settings shared by the first call and every tool-loop retry, so a
# tool-calling turn can't silently get different behaviour from a plain one.
GEN_KWARGS = dict(
    model=MODEL_NAME,
    tools=tools,
    reasoning_effort="none",
    max_completion_tokens=400,
)


def _rate_key(request):
    """Identify the visitor for rate limiting: Gradio session, then client IP."""
    if request is None:
        return "local"
    return getattr(request, "session_hash", None) or getattr(
        getattr(request, "client", None), "host", "unknown"
    )


def _generate_reply(messages, tool_calls_made):
    """Run the tool-calling loop and return (answer_text, total_tokens).

    Appends each tool name to `tool_calls_made` so the caller can log it. Lets
    any OpenAI error propagate so the caller can turn it into a visitor-safe
    message; never returns a partial or invented answer.
    """
    response = openai.chat.completions.create(messages=messages, **GEN_KWARGS)

    rounds = 0
    while response.choices[0].finish_reason == "tool_calls" and rounds < MAX_TOOL_ROUNDS:
        rounds += 1
        assistant_message = response.choices[0].message
        tool_calls_made.extend(tc.function.name for tc in assistant_message.tool_calls)
        results = handle_tool_calls(assistant_message.tool_calls)
        messages.append(assistant_message)
        messages.extend(results)
        response = openai.chat.completions.create(messages=messages, **GEN_KWARGS)

    if response.choices[0].finish_reason == "tool_calls":
        # Past the cap and still asking for tools. Drop tools and take whatever
        # text answer the model can give from the context it already has.
        log_event("tool_loop_capped", rounds=rounds)
        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            reasoning_effort="none",
            max_completion_tokens=400,
        )

    usage = getattr(response, "usage", None)
    return response.choices[0].message.content, getattr(usage, "total_tokens", None)


@spaces.GPU
def chat(message, history, request: gr.Request = None):
    """Send a message through the twin's tool-calling loop.

    Yields twice: first to show the user's bubble immediately and reveal
    the chat area, then again once the (non-streamed, so the response is
    always complete before it's shown) assistant reply is ready.
    """
    message = (message or "").strip()
    if not message:
        yield history, gr.update(), gr.update(), gr.update(), gr.update()
        return

    history = history + [{"role": "user", "content": message}]
    # An empty assistant turn renders Gradio's typing indicator while we wait.
    # It's replaced by the real answer on the final yield.
    yield (
        history + [{"role": "assistant", "content": ""}],
        "",
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=True),
    )

    req_id = new_request_id()
    started = time.monotonic()
    tool_calls_made = []

    def elapsed_ms():
        return round((time.monotonic() - started) * 1000)

    allowed, retry_after = ratelimit.check(_rate_key(request))
    if not allowed:
        log_event("rate_limited", req_id=req_id, retry_after=retry_after)
        answer = (
            "You've sent a lot of messages in a short time. Give me about "
            f"{retry_after} seconds and try again."
        )
        history = history + [{"role": "assistant", "content": answer}]
        yield (
            history,
            "",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
        )
        return

    log_event(
        "request_start",
        req_id=req_id,
        model=MODEL_NAME,
        message_chars=len(message),
        history_turns=len(history) - 1,
    )

    messages = system + history
    try:
        answer, total_tokens = _generate_reply(messages, tool_calls_made)
    except RateLimitError:
        answer = BUSY_REPLY
        log_event(
            "request_error",
            req_id=req_id,
            latency_ms=elapsed_ms(),
            tool_calls=tool_calls_made,
            error="RateLimitError",
        )
    except (APITimeoutError, APIError) as e:
        answer = ERROR_REPLY
        log_event(
            "request_error",
            req_id=req_id,
            latency_ms=elapsed_ms(),
            tool_calls=tool_calls_made,
            error=f"{type(e).__name__}: {e}",
        )
    except Exception as e:
        # Anything else (tool bug, bad response shape) still gets a calm reply
        # rather than a traceback rendered in the chat window.
        answer = ERROR_REPLY
        log_event(
            "request_error",
            req_id=req_id,
            latency_ms=elapsed_ms(),
            tool_calls=tool_calls_made,
            error=f"{type(e).__name__}: {e}",
        )
    else:
        log_event(
            "request_end",
            req_id=req_id,
            status="ok",
            latency_ms=elapsed_ms(),
            tool_rounds=len(tool_calls_made),
            tool_calls=tool_calls_made,
            answer_chars=len(answer or ""),
            total_tokens=total_tokens,
        )

    history = history + [{"role": "assistant", "content": answer}]
    yield (
        history,
        "",
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=True),
    )


with gr.Blocks(title=BRAND_NAME) as demo:
    with gr.Column(elem_id="app-shell"):
        with gr.Column(elem_id="content-area"):
            with gr.Column(elem_id="hero-section") as hero_section:
                gr.HTML(
                    f'<p id="hero-greeting">{HERO_GREETING}</p>'
                    f'<h1 id="hero-headline">{HERO_HEADLINE}</h1>'
                    f'<p id="hero-subtext">{HERO_SUBTEXT}</p>'
                )

            with gr.Row(elem_id="quick-prompts") as quick_prompts:
                prompt_cards = [
                    gr.Button(
                        prompt,
                        elem_classes=["prompt-card"],
                        variant="secondary",
                    )
                    for prompt in EXAMPLES
                ]

            with gr.Column(elem_id="chat-section", visible=False) as chat_section:
                chatbot = gr.Chatbot(
                    elem_id="chat-window",
                    show_label=False,
                    container=False,
                    autoscroll=True,
                )

        with gr.Row(elem_id="message-composer"):
            msg_input = gr.Textbox(
                elem_id="message-input",
                placeholder=INPUT_PLACEHOLDER,
                label="Message Kervintz's digital twin",
                show_label=False,
                container=False,
                autofocus=True,
                scale=1,
            )
            send_btn = gr.Button("Send", elem_id="send-button")

    outputs = [chatbot, msg_input, hero_section, quick_prompts, chat_section]

    msg_input.submit(chat, inputs=[msg_input, chatbot], outputs=outputs).then(
        lambda: None, None, None, js=FOCUS_JS
    )
    send_btn.click(chat, inputs=[msg_input, chatbot], outputs=outputs).then(
        lambda: None, None, None, js=FOCUS_JS
    )

    for card, prompt_text in zip(prompt_cards, EXAMPLES):
        card.click(lambda t=prompt_text: t, None, msg_input).then(
            chat, inputs=[msg_input, chatbot], outputs=outputs
        ).then(lambda: None, None, None, js=FOCUS_JS)

    demo.load(None, None, None, js=EMBED_JS)

demo.queue()

if __name__ == "__main__":
    demo.launch(css=CSS, theme=gr.themes.Base())
