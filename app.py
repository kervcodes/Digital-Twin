from openai import OpenAI
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from styles import CSS, EXAMPLES, FOCUS_JS, EMBED_JS
from dotenv import load_dotenv
import gradio as gr
import spaces

load_dotenv(override=True)

MODEL_NAME = "gpt-5.4-mini"

openai = OpenAI()

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]

BRAND_NAME = "Kervintz AI"
HERO_GREETING = "Hi, I'm Kervintz's AI digital twin"
HERO_HEADLINE = "What would you like to know?"
HERO_SUBTEXT = (
    "Ask about my professional background, technical experience, "
    "projects, or engineering approach."
)
INPUT_PLACEHOLDER = "Ask me anything about Kervintz's professional work"


@spaces.GPU
def respond(message, history):
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

    messages = system + history
    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools,
        reasoning_effort="none",
        max_completion_tokens=400,
    )

    while response.choices[0].finish_reason == "tool_calls":
        assistant_message = response.choices[0].message
        tool_calls = assistant_message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(assistant_message)
        messages.extend(results)
        response = openai.chat.completions.create(
            model=MODEL_NAME, messages=messages, tools=tools
        )

    answer = response.choices[0].message.content
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
        with gr.Row(elem_id="topbar"):
            gr.HTML(
                f'<div id="brand"><span id="brand-mark" aria-hidden="true">K</span>'
                f'<span id="brand-name">{BRAND_NAME}</span></div>'
            )

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

    msg_input.submit(respond, inputs=[msg_input, chatbot], outputs=outputs).then(
        lambda: None, None, None, js=FOCUS_JS
    )
    send_btn.click(respond, inputs=[msg_input, chatbot], outputs=outputs).then(
        lambda: None, None, None, js=FOCUS_JS
    )

    for card, prompt_text in zip(prompt_cards, EXAMPLES):
        card.click(lambda t=prompt_text: t, None, msg_input).then(
            respond, inputs=[msg_input, chatbot], outputs=outputs
        ).then(lambda: None, None, None, js=FOCUS_JS)

    demo.load(None, None, None, js=EMBED_JS)

demo.queue()

if __name__ == "__main__":
    demo.launch(css=CSS, theme=gr.themes.Base())
