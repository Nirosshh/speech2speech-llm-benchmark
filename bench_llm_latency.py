
"""
Benchmark first token and total latency for different LLM providers.

Providers:
- OpenAI GPT-4o-mini (streaming)
- Google Gemini (free or paid) (streaming)
- Hugging Face (Meta LLaMA 3 via Inference API) (no true streaming here, measure total only)

Use environment variables:
- OPENAI_API_KEY
- GOOGLE_API_KEY
- HF_API_TOKEN

Run:
python bench_llm_latency.py --n 5 --prompt "Explain what streaming means in simple terms."

Output:
- CSV file 'results_latency.csv' with columns: provider, model, ttfb_s, total_s, ok, error
"""
import os, time, argparse, csv
from utils_timing import FirstTokenTimer

def bench_openai(prompt: str):
    """Test OpenAI streaming for GPT-4o-mini."""
    import openai
    client = openai.OpenAI() if hasattr(openai, "OpenAI") else None
    if client is None:
        from openai import OpenAI
        client = OpenAI()

    ft = FirstTokenTimer()
    ft.start()
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
            stream=True
        )
        seen_any = False
        text = []
        for ev in stream:
            delta = ev.choices[0].delta
            if not seen_any and getattr(delta, "content", None):
                seen_any = True
                ft.mark_first_token()
            if getattr(delta, "content", None):
                text.append(delta.content)
        total = time.monotonic() - ft.started_at
        return {"provider":"openai","model":"gpt-4o-mini","ttfb_s":round(ft.ttfb or -1, 3),"total_s":round(total,3),"ok":True,"error":""}
    except Exception as e:
        return {"provider":"openai","model":"gpt-4o-mini","ttfb_s":None,"total_s":None,"ok":False,"error":str(e)}

def bench_gemini(prompt: str):
    """Test Google Gemini streaming for speed."""
    import google.generativeai as genai
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return {"provider":"gemini","model":"gemini-1.5-flash","ttfb_s":None,"total_s":None,"ok":False,"error":"GOOGLE_API_KEY not set"}
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    ft = FirstTokenTimer()
    ft.start()
    try:
        stream = model.generate_content(prompt, stream=True)
        seen_any = False
        text = []
        for chunk in stream:
            ctext = getattr(chunk, "text", "")
            if ctext:
                if not seen_any:
                    seen_any = True
                    ft.mark_first_token()
                text.append(ctext)
        total = time.monotonic() - ft.started_at
        return {"provider":"gemini","model":"gemini-1.5-flash","ttfb_s":round(ft.ttfb or -1, 3),"total_s":round(total,3),"ok":True,"error":""}
    except Exception as e:
        return {"provider":"gemini","model":"gemini-1.5-flash","ttfb_s":None,"total_s":None,"ok":False,"error":str(e)}

def bench_hf(prompt: str):
    """Hugging Face text-generation Inference API (no token stream)."""
    import requests, json, time
    token = os.environ.get("HF_API_TOKEN")
    if not token:
        return {"provider":"huggingface","model":"Meta-Llama-3-8B-Instruct","ttfb_s":None,"total_s":None,"ok":False,"error":"HF_API_TOKEN not set"}
    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = {"Authorization": f"Bearer {token}", "Accept":"application/json"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 64, "temperature": 0.3}}
    start = time.monotonic()
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        total = time.monotonic() - start
        return {"provider":"huggingface","model":"Meta-Llama-3-8B-Instruct","ttfb_s":None,"total_s":round(total,3),"ok":True,"error":""}
    except Exception as e:
        return {"provider":"huggingface","model":"Meta-Llama-3-8B-Instruct","ttfb_s":None,"total_s":None,"ok":False,"error":str(e)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=3, help="repetitions per provider")
    ap.add_argument("--prompt", type=str, default="Explain streaming in simple words.", help="test prompt")
    args = ap.parse_args()

    rows = []
    for i in range(args.n):
        rows.append(bench_openai(args.prompt))
        rows.append(bench_gemini(args.prompt))
        rows.append(bench_hf(args.prompt))

    out = "results_latency.csv"
    import csv
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["provider","model","ttfb_s","total_s","ok","error"])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Wrote {out} with {len(rows)} rows.")

if __name__ == "__main__":
    main()
