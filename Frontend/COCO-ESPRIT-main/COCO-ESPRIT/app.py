from flask import Flask, request, jsonify, render_template
import json
from chat import get_response
from flask_cors import CORS
import easyocr
import os
from PIL import Image
import pandas as pd
from sklearn import linear_model
import numpy as np

app = Flask(__name__)
CORS(app, supports_credentials=True, origins='http://localhost:4200')

# Load CO2 prediction model
print("Loading CO2 prediction model...")
data = pd.read_csv("FuelConsumption.csv")
data_select = data[['ENGINESIZE', 'CYLINDERS', 'FUELCONSUMPTION_CITY', 'FUELCONSUMPTION_HWY', 'FUELCONSUMPTION_COMB', 'CO2EMISSIONS']]
regr = linear_model.LinearRegression()
x = np.asanyarray(data_select[["ENGINESIZE", "CYLINDERS", "FUELCONSUMPTION_CITY", "FUELCONSUMPTION_HWY"]])
y = np.asanyarray(data_select[["CO2EMISSIONS"]])
regr.fit(x, y)
print("CO2 model loaded successfully!")

# Define the list of bad words
bad_words = [
    "Fuck", "Shit", "Asshole", "Bitch", "Bastard", "Cunt", "Dick", "Pussy",
    "Motherfucker", "Cock", "Twat", "Wanker", "Slut", "Whore", "Arsehole",
    "Douchebag", "Faggot", "Nigger", "Prick", "Dumbass"
]

# Initialize EasyOCR reader for English
reader = easyocr.Reader(['en'])

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

def load_intents():
    with open('intents.json', 'r') as file:
        intents = json.load(file)
    return intents

intents = load_intents()

#@app.get("/")
#def index_get():
#    return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    response = get_response(text)
    message = {"answer" : response}
    return jsonify(message)

@app.route('/CO2', methods=['POST'])
def predict_co2():
    data = request.json
    engine_size = data['Engine Size']
    cylinder_num = data['Cylinder Number']
    fuelconsumption_city = data['Fuel Consumption in City']
    fuelconsumption_hwy = data['Fuel Consumption in Highway']
    
    df = pd.DataFrame({
        'Engine Size': [engine_size],
        'Cylinder Number': [cylinder_num],
        'Fuel Consumption in City': [fuelconsumption_city],
        'Fuel Consumption in Highway': [fuelconsumption_hwy]
    })

    # Predict CO2 emissions
    prediction = regr.predict(df)

    return jsonify({'prediction': prediction[0].tolist()})

if __name__ == '__main__':
    app.run(debug=True)
