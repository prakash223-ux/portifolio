from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ✅ Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///contacts.db")
# Fix PostgreSQL URL scheme for SQLAlchemy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ✅ Contact Model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "subject": self.subject,
            "message": self.message,
            "created_at": self.created_at.isoformat()
        }

# ✅ Create tables
with app.app_context():
    db.create_all()

# ✅ Root route
@app.route("/")
def home():
    return jsonify({"status": "Backend running ✅", "version": "1.0"})

# ✅ Health check
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

# ✅ Form submit route
@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "No JSON data received"}), 400

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        subject = data.get("subject", "").strip()
        message = data.get("message", "").strip()

        # ✅ Validation
        if not all([name, email, phone, message]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # ✅ Create and save contact
        contact = Contact(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        db.session.add(contact)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Saved successfully",
            "id": contact.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# ✅ Get all contacts (admin endpoint)
@app.route("/contacts", methods=["GET"])
def get_contacts():
    try:
        contacts = Contact.query.all()
        return jsonify({
            "status": "success",
            "count": len(contacts),
            "data": [contact.to_dict() for contact in contacts]
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ✅ Export to Excel endpoint
@app.route("/export", methods=["GET"])
def export():
    try:
        import pandas as pd
        contacts = Contact.query.all()
        
        if not contacts:
            return jsonify({"status": "error", "message": "No data to export"}), 400
        
        data = [contact.to_dict() for contact in contacts]
        df = pd.DataFrame(data)
        
        filename = "contacts_export.xlsx"
        df.to_excel(filename, index=False)
        
        return jsonify({
            "status": "success",
            "message": f"Exported {len(contacts)} contacts",
            "file": filename
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)