from flask import Flask, request, jsonify
import openai
import threading

openai.api_key = "YOUR_OPENAI_KEY"

app = Flask(__name__)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    print(f"User: {user_msg}")

    response_text = []
    def stream_response():
        stream = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_msg}],
            stream=True
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.get("content")
            if delta:
                response_text.append(delta)

    t = threading.Thread(target=stream_response)
    t.start()
    t.join()

    return jsonify({"response": "".join(response_text)})

if __name__ == "__main__":
    app.run(debug=True)
