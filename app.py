from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual OpenRouter API key
OPENROUTER_API_KEY = "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"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_msg = request.json.get("message")

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",  # Important for free tier
                "X-Title": "FlaskChatApp"
            },
            json={
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": [
                    {"role": "user", "content": user_msg}
                ]
            }
        )

        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
