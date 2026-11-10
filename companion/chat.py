"""Chat with the companion in the terminal, using a local model served by Ollama.

Run from the repo root:

    python -m companion.chat

Settings (environment variables):
    COMPANION_MODEL   model name to use (default: gemma3:4b)
    OLLAMA_URL        where Ollama is listening (default: http://localhost:11434)
"""

import json
import os
import sys
import urllib.error
import urllib.request

from .character import SYSTEM_PROMPT

MODEL = os.environ.get("COMPANION_MODEL", "gemma3:4b")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")


def stream_reply(messages):
    """Send the conversation to Ollama and yield the reply piece by piece."""
    body = json.dumps({"model": MODEL, "messages": messages, "stream": True}).encode("utf-8")
    request = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request) as response:
        for line in response:
            if not line.strip():
                continue
            chunk = json.loads(line)
            if "error" in chunk:
                raise RuntimeError(chunk["error"])
            yield chunk.get("message", {}).get("content", "")
            if chunk.get("done"):
                break


def main():
    # Windows consoles may not default to UTF-8; models often emit non-ASCII text.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print(f"Talking to {MODEL}. Type 'quit' or press Ctrl+C to leave.\n")

    while True:
        try:
            user_text = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not user_text:
            continue
        if user_text.lower() in {"quit", "exit"}:
            return 0

        messages.append({"role": "user", "content": user_text})
        reply_parts = []
        print("companion> ", end="", flush=True)
        try:
            for piece in stream_reply(messages):
                reply_parts.append(piece)
                print(piece, end="", flush=True)
        except urllib.error.HTTPError as error:
            print(f"\nOllama returned an error ({error.code}).")
            if error.code == 404:
                print(f"The model may not be downloaded yet. Try: ollama pull {MODEL}")
            return 1
        except urllib.error.URLError:
            print(f"\nCould not reach Ollama at {OLLAMA_URL}. Is it installed and running?")
            return 1
        except RuntimeError as error:
            print(f"\nOllama reported: {error}")
            return 1
        except KeyboardInterrupt:
            print("\n(stopped)")
            messages.pop()
            continue
        print("\n")
        messages.append({"role": "assistant", "content": "".join(reply_parts)})


if __name__ == "__main__":
    sys.exit(main())
