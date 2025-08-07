from flask import Flask, request, jsonify
import openai
import os

# Tạo Flask app, trùng tên với `app` trong Procfile
app = Flask(__name__)

# Lấy API key từ biến môi trường hoặc file key.txt
if os.path.exists("key.txt"):
    with open("key.txt") as f:
        openai.api_key = f.read().strip()
else:
    openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Chatbot Bất động sản đang chạy!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "Không có nội dung"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # hoặc gpt-4 nếu bạn có quyền
            messages=[
                {"role": "system", "content": "Bạn là chatbot tư vấn bất động sản."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message['content']
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Để local chạy được
if __name__ == '__main__':
    app.run(debug=True)
