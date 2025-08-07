import os
from flask import Flask, render_template_string, request
import openai

# Khởi tạo Flask
app = Flask(__name__)

# Lấy API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

# Giao diện HTML đơn giản
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Chatbot Bất động sản</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f2f2f2; }
        .chatbox {
            width: 400px; margin: 80px auto; padding: 20px;
            background: white; border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        input[type="text"] {
            width: 100%; padding: 10px; border: 1px solid #ccc;
            border-radius: 4px; margin-top: 10px;
        }
        button {
            background: #007bff; color: white; border: none;
            padding: 10px 16px; margin-top: 10px; border-radius: 4px;
            cursor: pointer;
        }
        .response {
            margin-top: 15px; padding: 10px;
            background: #e9f5ff; border-left: 4px solid #007bff;
        }
    </style>
</head>
<body>
    <div class="chatbox">
        <h2>💬 Chatbot Bất động sản</h2>
        <form method="POST">
            <input type="text" name="message" placeholder="Nhập câp c\xe2u hỏi...">
            <button type="submit">Gửi</button>
        </form>
        {% if response %}
        <div class="response">
            <strong>Bot:</strong> {{ response }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# Route chính
@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form.get("message", "")
        if user_input:
            try:
                result = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Bạn là một chuyên gia bất động sản, trả lời ngắn gọn và chính xác."},
                        {"role": "user", "content": user_input}
                    ]
                )
                response = result["choices"][0]["message"]["content"]
            except Exception as e:
                response = f"Lỗi khi gọi OpenAI API: {str(e)}"
    return render_template_string(HTML_TEMPLATE, response=response)

# Khởi chạy ứng dụng
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
