import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"

client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/')
def home():
    return "BDS Chatbot is running!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Bạn là trợ lý bất động sản, trả lời ngắn gọn, dễ hiểu."},
            {"role": "user", "content": message}
        ]
    )

    return jsonify({"reply": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
