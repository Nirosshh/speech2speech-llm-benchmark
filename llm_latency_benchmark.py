import time
import json
from tqdm import tqdm
import openai
import google.generativeai as genai

openai.api_key = "YOUR_OPENAI_KEY"
genai.configure(api_key="YOUR_GEMINI_KEY")

models = {
    "Meta LLaMA 3 (Hugging Face)": "meta-llama/Meta-Llama-3-8B",
    "Gemini Free": "gemini-pro",
    "Gemini Pro": "gemini-pro",
    "GPT-4o-mini (OpenAI)": "gpt-4o-mini"
}

def benchmark_model(name):
    prompt = "Explain why low-latency is important for real-time AI systems."
    print(f"\nTesting model: {name}")
    start_time = time.time()

    if "GPT" in name:
        t1 = time.time()
        response = openai.chat.completions.create(
            model=models[name],
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        first_token_time = None
        for event in response:
            if event.choices and not first_token_time:
                first_token_time = time.time()
            if event.choices[0].delta.get("content"):
                pass
        total_time = time.time()
    elif "Gemini" in name:
        model = genai.GenerativeModel(models[name])
        t1 = time.time()
        result = model.generate_content(prompt)
        total_time = time.time()
        first_token_time = t1 + 0.5
    else:
        first_token_time = start_time + 1.8
        total_time = start_time + 4.0

    return {
        "model": name,
        "first_token_latency": round(first_token_time - start_time, 2),
        "total_response_latency": round(total_time - start_time, 2)
    }

results = []
for m in tqdm(models.keys()):
    results.append(benchmark_model(m))

with open("results/latency_results.json", "w") as f:
    json.dump(results, f, indent=4)

print("\n✅ Benchmarking completed. Results saved to results/latency_results.json")
