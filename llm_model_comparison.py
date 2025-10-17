import json
import pandas as pd

with open("results/latency_results.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)
print("\nModel Latency Comparison:\n")
print(df.to_string(index=False))
best_model = df.loc[df['total_response_latency'].idxmin()]
print(f"\n🏆 Fastest Model: {best_model['model']} "
      f"({best_model['first_token_latency']}s / {best_model['total_response_latency']}s)")
