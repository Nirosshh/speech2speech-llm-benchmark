
"""
Stream tokens from GPT-4o-mini and measure time to first token and total time.
Requires OPENAI_API_KEY.
"""
import time
from utils_timing import FirstTokenTimer

def main():
    import openai
    client = openai.OpenAI() if hasattr(openai, "OpenAI") else None
    if client is None:
        from openai import OpenAI
        client = OpenAI()

    prompt = "Give me 3 short tips to improve English speaking in daily life."
    ft = FirstTokenTimer()
    ft.start()
    seen_any = False
    text = []
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
            stream=True
        )
        for ev in stream:
            delta = ev.choices[0].delta
            if getattr(delta, "content", None):
                if not seen_any:
                    seen_any = True
                    ft.mark_first_token()
                piece = delta.content
                text.append(piece)
                print(piece, end="", flush=True)
        print("\\n---")
        print(f"First token: {round(ft.ttfb or -1,3)} s, Total: {round(time.monotonic()-ft.started_at,3)} s")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
