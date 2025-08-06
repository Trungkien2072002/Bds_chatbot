from flask import Flask, request, jsonify
import os
import openai

# Khởi tạo Flask app
app = Flask(__name__)

# Lấy API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

# Route kiểm tra hoạt động
@app.route("/", methods=["GET"])
def home():
    return "Chatbot BDS đang chạy!"

# Route chat với bot
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"error": "Thiếu tin nhắn"}), 400

        # Gọi API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý Bất động sản chuyên nghiệp."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Chạy local
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
