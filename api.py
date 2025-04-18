# api.py

import joblib

vectorizer = joblib.load("model/tfidf_vectorizer.pkl")
model = joblib.load("model/random_forest_model.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

def predict_category(masked_email):
    vec = vectorizer.transform([masked_email])
    pred = model.predict(vec)
    return label_encoder.inverse_transform(pred)[0]
