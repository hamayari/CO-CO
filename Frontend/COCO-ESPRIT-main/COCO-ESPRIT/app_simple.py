from flask import Flask, request, jsonify
from flask_cors import CORS
import easyocr
from PIL import Image

app = Flask(__name__)
CORS(app, supports_credentials=True, origins='http://localhost:4200')

# Define the list of bad words
bad_words = [
    "Fuck", "Shit", "Asshole", "Bitch", "Bastard", "Cunt", "Dick", "Pussy",
    "Motherfucker", "Cock", "Twat", "Wanker", "Slut", "Whore", "Arsehole",
    "Douchebag", "Faggot", "Nigger", "Prick", "Dumbass"
]

# Initialize EasyOCR reader for English
print("Initializing EasyOCR... This may take a moment...")
reader = easyocr.Reader(['en'])
print("EasyOCR initialized successfully!")

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        img = Image.open(file)
        results = reader.readtext(img)
        detected_text = ' '.join(result[1] for result in results)
        contains_bad_word = any(word in detected_text for word in bad_words)
        return jsonify({'detected_text': detected_text, 'contains_bad_word': contains_bad_word}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/predict', methods=['POST'])
def predict():
    # Simple response without chatbot
    return jsonify({"answer": "Chatbot is currently unavailable. Please check back later."}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Server is running"}), 200

if __name__ == '__main__':
    print("Starting Flask server on http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
