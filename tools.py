import json
import os
import requests
from dotenv import load_dotenv
from obs import log_event

load_dotenv(override=True)

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")

pushover_url = "https://api.pushover.net/1/messages.json"

# One structured line at import instead of the course's four print()s, so the
# Space logs record whether notifications can work at all.
log_event(
    "pushover_config",
    user_set=bool(pushover_user),
    user_prefix_ok=bool(pushover_user and pushover_user.startswith("u")),
    token_set=bool(pushover_token),
    token_prefix_ok=bool(pushover_token and pushover_token.startswith("a")),
)


def push(message):
    """Send a Pushover notification. Returns True only on a confirmed 200.

    Never raises: a notification failure must not take down the tool call or
    the conversation. Missing credentials, a network error, or a non-200
    response are all logged and reported as False.
    """
    if not (pushover_user and pushover_token):
        log_event("push_skipped", reason="credentials not configured")
        return False
    try:
        payload = {"user": pushover_user, "token": pushover_token, "message": message}
        response = requests.post(pushover_url, data=payload, timeout=10)
    except requests.RequestException as e:
        log_event("push_error", error=f"{type(e).__name__}: {e}")
        return False
    if response.status_code != 200:
        log_event("push_error", status=response.status_code, body=response.text[:200])
        return False
    return True


def record_user_email(email, name="Name not provided", notes="not provided"):
    ok = push(f"Recording interest from {name} with email {email} and notes {notes}")
    return "OK" if ok else "Error"


def record_unknown_question(question):
    ok = push(f"Recording {question} asked that I couldn't answer")
    return "OK" if ok else "Error"


record_user_email_json = {
    "name": "record_user_email",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {
                "type": "string",
                "description": "Any additional info about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_email_json},
    {"type": "function", "function": record_unknown_question_json},
]

tool_map = {
    "record_user_email": record_user_email,
    "record_unknown_question": record_unknown_question,
}


def handle_tool_calls(tool_calls):
    """Run each requested tool and return one tool message per call.

    A failing tool yields an "Error" result for that call instead of raising,
    so the model still gets a well-formed response for every tool_call_id and
    the conversation can continue.
    """
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        try:
            arguments = json.loads(tool_call.function.arguments)
            tool = tool_map.get(tool_name)
            result = tool(**arguments) if tool else "Unknown tool: " + tool_name
        except Exception as e:
            log_event("tool_error", tool=tool_name, error=f"{type(e).__name__}: {e}")
            result = "Error"
        log_event("tool_call", tool=tool_name, result=result)
        results.append(
            {"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id}
        )
    return results
