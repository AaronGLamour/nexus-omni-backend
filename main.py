from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # تفعيل CORS لجميع المسارات والطلبات

@app.route("/")
def home():
    return jsonify({
        "message": "Nexus Omni Backend is running smoothly on PythonAnywhere!",
        "status": "success"
    })

@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Nexus Omni"
    })

@app.route("/api/v1/data", methods=["POST"])
def process_data():
    data = request.get_json()
    return jsonify({
        "status": "success",
        "received": data
    })

if __name__ == "__main__":
    app.run(debug=True)