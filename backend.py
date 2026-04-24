from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os

# 🔐 Load .env
load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")

print("FINAL KEY:", repr(api_key))

if not api_key:
    raise Exception("❌ GROQ_API_KEY not found in .env")

# 🤖 Groq client
client = Groq(api_key=api_key)

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"response": "No message received"})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response.choices[0].message.content

        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)