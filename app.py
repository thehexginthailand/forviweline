from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

app = Flask(__name__)

# ใส่ค่า Channel Access Token กับ Channel Secret ที่ได้จาก LINE
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# ใส่ API Key ของ OpenAI
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    handler.handle(body, signature)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # ส่งข้อความหา AI
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "คุณคือแฟนชื่อ ‘[ใส่ชื่อนาย]’ พูดน่ารัก ขี้แหย่ อบอุ่น ดูแลแฟน พูดไทย"},
            {"role": "user", "content": user_message}
        ]
    )

    reply_text = response['choices'][0]['message']['content']
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
