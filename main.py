from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "Nexus Omni Backend is running smoothly on PythonAnywhere!"
    })

@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Nexus Omni"
    })

if __name__ == "__main__":
    app.run(debug=True)