from flask import Flask, request, render_template_string
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

html_template = """
<!doctype html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Bất động sản</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f1f1;
            padding: 30px;
            max-width: 600px;
            margin: auto;
        }
        h2 {
            color: #333;
        }
        .chat-box {
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .user-input {
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            margin-bottom: 10px;
        }
        .submit-btn {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        .response {
            margin-top: 20px;
            background: #e8f0fe;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }
    </style>
</head>
<body>
    <div class="chat-box">
        <h2>💬 Chatbot Bất động sản</h2>
        <form method="post">
            <input name="user_input" class="user-input" placeholder="Nhập câu hỏi về bất động sản..." autofocus>
            <button type="submit" class="submit-btn">Gửi</button>
        </form>
        {% if response %}
            <div class="response">
                <strong>Bot trả lời:</strong><br>{{ response }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def chatbot():
    response = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia tư vấn bất động sản."},
                {"role": "user", "content": user_input},
            ]
        )
        response = res["choices"][0]["message"]["content"]
    return render_template_string(html_template, response=response)

if __name__ == "__main__":
    app.run(debug=True)
