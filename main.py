import os
import librosa
import numpy as np
import pandas as pd
import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the trained model
model = joblib.load("model.pkl")

# Load scaler if available
scaler_path = "scaler.pkl"
scaler = joblib.load(scaler_path) if os.path.exists(scaler_path) else None

# Feature extraction function
def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=16000)

    # Jitter and Shimmer approximations
    jitter = np.mean(librosa.feature.zero_crossing_rate(y=y))
    shimmer = np.mean(librosa.feature.rms(y=y))

    # HNR & NHR approximations
    harmonic, percussive = librosa.effects.hpss(y)
    hnr = np.mean(harmonic) / (np.mean(np.abs(y - harmonic)) + 1e-6)
    nhr = np.mean(percussive) / (np.mean(np.abs(y - percussive)) + 1e-6)

    # Spectral features
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)

    # Feature dictionary
    features = {
        "MDVP:Fo(Hz)": np.mean(spectral_centroid),
        "MDVP:Fhi(Hz)": np.max(spectral_centroid),
        "MDVP:Flo(Hz)": np.min(spectral_centroid),
        "MDVP:Jitter(%)": jitter,
        "MDVP:Jitter(Abs)": np.abs(np.diff(y)).mean(),
        "MDVP:RAP": jitter / 2,
        "MDVP:PPQ": jitter / 4,
        "Jitter:DDP": jitter * 3,
        "MDVP:Shimmer": shimmer,
        "MDVP:Shimmer(dB)": 20 * np.log10(shimmer + 1e-6),
        "MDVP:APQ": shimmer / 2,
        "Shimmer:APQ3": shimmer / 3,
        "Shimmer:APQ5": shimmer / 5,
        "Shimmer:DDA": shimmer * 3,
        "NHR": nhr,
        "HNR": hnr,
        "spread1": np.mean(spectral_bandwidth),
        "spread2": np.std(spectral_rolloff),
        "PPE": np.std(y) / (np.mean(y) + 1e-6),
        "RPDE": 0.4,  # Placeholder
        "DFA": 0.7,   # Placeholder
        "D2": 2.4     # Placeholder
    }

    features_df = pd.DataFrame([features])

    # Match training feature order
    features_df = features_df[model.feature_names_in_]

    # Scale if needed
    if scaler:
        features_df = pd.DataFrame(scaler.transform(features_df), columns=features_df.columns)

    print("Extracted features:\n", features_df)
    return features_df

# Prediction function
def predict_parkinsons(features):
    prediction = model.predict(features)[0]
    return "Parkinson's Disease Detected" if prediction == 0 else "No Parkinson's Detected"

# Web route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "audio" not in request.files or request.files["audio"].filename == "":
            return render_template("index.html", message="No file selected!")

        file = request.files["audio"]
        upload_path = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(upload_path)

        features = extract_features(upload_path)
        result = predict_parkinsons(features)

        return render_template("index.html", message=result)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
app.py
Displaying app.py
