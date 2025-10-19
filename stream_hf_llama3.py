
"""
Call Hugging Face Inference API for Meta-Llama-3 Instruct.
This is not true token streaming in this simple example, but shows total time.
Requires HF_API_TOKEN.
"""
import os, time, requests

def main():
    token = os.environ.get("HF_API_TOKEN")
    if not token:
        print("HF_API_TOKEN not set")
        return
    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = {"Authorization": f"Bearer {token}", "Accept":"application/json"}
    payload = {"inputs": "Give me 3 short tips to improve English speaking in daily life.",
               "parameters": {"max_new_tokens": 64, "temperature": 0.3}}
    start = time.monotonic()
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        total = time.monotonic() - start
        print(r.json())
        print("---")
        print(f"Total: {round(total,3)} s")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
