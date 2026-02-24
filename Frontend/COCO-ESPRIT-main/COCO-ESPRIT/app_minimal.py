from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, origins='http://localhost:4200')

@app.route('/upload', methods=['POST'])
def upload_file():
    return jsonify({
        'message': 'OCR service temporarily unavailable',
        'detected_text': '',
        'contains_bad_word': False
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    text = request.get_json().get("message", "")
    # Simple echo response
    return jsonify({"answer": f"You said: {text}. (Chatbot AI is temporarily unavailable)"}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Server is running"}), 200

if __name__ == '__main__':
    print("=" * 60)
    print("Flask server starting on http://127.0.0.1:5001")
    print("Note: Chatbot and OCR features require PyTorch")
    print("=" * 60)
    app.run(debug=True, port=5001)
