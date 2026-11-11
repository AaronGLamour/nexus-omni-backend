from flask import Flask, jsonify, request

app = Flask(__name__)

# مسار الصفحة الرئيسية للتأكد من العمل
@app.route("/")
def home():
    return jsonify({
        "message": "Nexus Omni Backend is running smoothly on PythonAnywhere!",
        "status": "success"
    })

# مسار فحص الحالة
@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Nexus Omni"
    })

# 🚀 مسار استقبال البيانات الجديد (POST Request)
@app.route("/api/v1/data", methods=["POST"])
def process_data():
    data = request.get_json()
    # يمكنك هنا معالجة البيانات أو حفظها في قاعدة البيانات
    return jsonify({
        "status": "success",
        "received": data
    })

if __name__ == "__main__":
    app.run(debug=True)