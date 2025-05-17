from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Initialize app
app = Flask(__name__)

# Load model and tokenizer
model = load_model('lstm_model.h5')
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Set max length same as during training
MAX_SEQUENCE_LENGTH = 300

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    confidence = None

    if request.method == 'POST':
        news_text = request.form['news']

        if news_text.strip():
            # Preprocess input
            seq = tokenizer.texts_to_sequences([news_text])
            padded = pad_sequences(seq, maxlen=MAX_SEQUENCE_LENGTH)

            # Predict
            prob = model.predict(padded)[0][0]
            prediction = 'FAKE' if prob <= 0.6 else 'REAL'
            confidence = round(prob * 100, 2) if prediction == 'REAL' else round((1 - prob) * 100, 2)

    return render_template('index.html', prediction=prediction, confidence=confidence)

if __name__ == '__main__':
    app.run(debug=True)
