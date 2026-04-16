from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

FILE_PATH = "contact_data.xlsx"

# Ensure Excel file exists
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=["Name", "Email", "Phone", "Subject", "Message"])
    df.to_excel(FILE_PATH, index=False)

# ✅ Root route (fix Not Found issue)
@app.route("/")
def home():
    return "Backend running ✅"

# ✅ Form submit route
@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "No JSON data received"}), 400

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        subject = data.get("subject")
        message = data.get("message")

        # ✅ Basic validation
        if not all([name, email, phone, message]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        new_row = pd.DataFrame([{
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Subject": subject,
            "Message": message
        }])

        # ✅ Safe read (prevents crash)
        try:
            existing = pd.read_excel(FILE_PATH)
        except:
            existing = pd.DataFrame(columns=["Name", "Email", "Phone", "Subject", "Message"])

        updated = pd.concat([existing, new_row], ignore_index=True)
        updated.to_excel(FILE_PATH, index=False)

        return jsonify({"status": "success", "message": "Saved successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)