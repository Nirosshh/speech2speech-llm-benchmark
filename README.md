
# LLM Evidence Pack

This folder contains clean scripts that prove your testing of LLMs and a real-time streaming architecture.

## Files

- `bench_llm_latency.py` — runs latency benchmarks for OpenAI GPT-4o-mini, Google Gemini 1.5 Flash, and Hugging Face Meta-Llama-3 Instruct. Writes `results_latency.csv`.
- `stream_gpt4o_mini.py` — streams tokens from GPT-4o-mini and prints time to first token and total time.
- `stream_gemini.py` — streams tokens from Gemini 1.5 Flash and prints time to first token and total time.
- `stream_hf_llama3.py` — calls Hugging Face Inference API for Meta-Llama-3 (total time only).
- `utils_timing.py` — helper for timing and first token measurement.
- `app_socketio_stub.py` — small Flask + Socket.IO stub that shows real-time events and token streaming.

## Setup

```bash
pip install openai google-generativeai requests flask flask-socketio
```

Set your API keys as environment variables:

```powershell
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."
$env:GOOGLE_API_KEY = "AIza..."
$env:HF_API_TOKEN   = "hf_..."
```

## Run benchmarks

```bash
python bench_llm_latency.py --n 5 --prompt "Explain streaming in simple words."
type results_latency.csv
```

CSV columns:
- provider
- model
- ttfb_s
- total_s
- ok
- error

## Stream tests

```bash
python stream_gpt4o_mini.py
python stream_gemini.py
python stream_hf_llama3.py
```

## Real-time architecture stub

```bash
python app_socketio_stub.py
```

Connect a Socket.IO client to see events: `partial_transcript`, `llm_token`, `llm_done`.

## Notes

<<<<<<< HEAD
- Latency depends on network and time of day. Run each test several times and report the average.
=======
- Do not commit your API keys.
- Latency depends on network and time of day. Run each test several times and report the average.
- You can commit `results_latency.csv` as evidence with your slide screenshots.
>>>>>>> 609e19c (Initial commit - personal LLM latency benchmark project)
