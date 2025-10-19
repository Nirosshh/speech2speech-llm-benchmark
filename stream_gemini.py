
"""
Stream tokens from Gemini 1.5 Flash and measure latency.
Requires GOOGLE_API_KEY.
"""
import os, time
from utils_timing import FirstTokenTimer
import google.generativeai as genai

def main():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not set")
        return
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = "Give me 3 short tips to improve English speaking in daily life."
    ft = FirstTokenTimer()
    ft.start()
    seen_any = False
    text = []
    try:
        stream = model.generate_content(prompt, stream=True)
        for chunk in stream:
            ctext = getattr(chunk, "text", "")
            if ctext:
                if not seen_any:
                    seen_any = True
                    ft.mark_first_token()
                print(ctext, end="", flush=True)
                text.append(ctext)
        print("\\n---")
        print(f"First token: {round(ft.ttfb or -1,3)} s, Total: {round(time.monotonic()-ft.started_at,3)} s")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
