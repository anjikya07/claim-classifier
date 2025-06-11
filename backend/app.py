
from flask import Flask, request, jsonify
import sqlite3
import joblib
import numpy as np

app = Flask(__name__)

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect('claims.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS claims (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    claim_text TEXT,
                    claims_count INTEGER,
                    previous_denials INTEGER,
                    profile_score REAL
                )''')
    conn.commit()
    conn.close()

init_db()

# Load ML model
model = joblib.load("model.pkl")

@app.route("/api/classify-claim", methods=["POST"])
def classify_claim():
    data = request.json
    claim_text = data.get("claim_text", "")
    history = data.get("claimant_history", {})
    claims_count = history.get("claims_count", 0)
    previous_denials = history.get("previous_denials", 0)
    profile_score = history.get("profile_score", 0.5)

    # Save to DB
    conn = sqlite3.connect('claims.db')
    c = conn.cursor()
    c.execute("INSERT INTO claims (claim_text, claims_count, previous_denials, profile_score) VALUES (?, ?, ?, ?)",
              (claim_text, claims_count, previous_denials, profile_score))
    conn.commit()
    conn.close()

    # ML Prediction
    input_features = np.array([[claims_count, previous_denials, profile_score]])
    prediction = model.predict(input_features)[0]
    proba = model.predict_proba(input_features)[0][1]

    return jsonify({
        "result": "Respond" if prediction == 1 else "Reject",
        "confidence": round(float(proba), 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
