from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# ===== تنظیمات ربات =====
BOT_TOKEN = '1066259520:xG6U1dbQ981cGiGSNHxePlExqwOKsSQnwEY'
CHAT_ID = '1416395651'
BALE_API = f'https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage'

# ===== مسیر اصلی: نمایش فایل index.html =====
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# ===== مسیر /send: ارسال پیام به ربات =====
@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'متن خالی'}), 400
    try:
        r = requests.post(BALE_API, json={'chat_id': CHAT_ID, 'text': text}, timeout=10)
        result = r.json()
        if r.status_code == 200 and result.get('ok'):
            return jsonify({'success': True})
        else:
            return jsonify({'error': result.get('description', 'خطا')}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== اجرای برنامه =====
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
