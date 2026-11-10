# companion

A local AI desktop companion with a face and a voice. Everything runs on your own machine: no cloud, no API keys.

> Working name. Early days: right now it chats in the terminal.

## What works today

- Terminal chat with a local model through [Ollama](https://ollama.com)

## Coming next

- A voice (text to speech)
- Ears (speech to text)
- A face: a small always-on-top window with eyes that react

## Requirements

- Windows 10/11 or Ubuntu
- Python 3.11 or newer
- [Ollama](https://ollama.com/download)
- A GPU with about 6 GB of VRAM is recommended; it will run on CPU, slowly

## Quick start

```bash
ollama pull gemma3:4b
```

```bash
python -m companion.chat
```

On Windows, if `python` opens the Microsoft Store, use `py -m companion.chat` instead.

Use a different model by setting `COMPANION_MODEL`, for example `llama3.2:3b` on a smaller GPU.

## Change the personality

Edit [companion/character.py](companion/character.py).

## License

MIT
