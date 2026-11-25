from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from functools import wraps
from datetime import datetime
from pathlib import Path
import shutil
from datetime import datetime

def run_auto_backup():
    try:
        db_f = BASE_DIR / "nexus_omni.db"
        if db_f.exists():
            bk = BASE_DIR / "backups"
            bk.mkdir(exist_ok=True)
            stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            shutil.copy2(db_f, bk / f"nexus_omni_{stamp}.db")
            old_files = sorted(bk.glob("nexus_omni_*.db"), key=lambda x: x.stat().st_mtime, reverse=True)[7:]
            for old in old_files:
                old.unlink()
    except Exception as e:
        print(f"Backup warning: {e}")

from waitress import serve
import os
import json
import csv
import io

BASE_DIR = Path(__file__).parent

env_path = BASE_DIR / '.env'
if env_path.exists():
    for line in env_path.read_text(encoding='utf-8').splitlines():
        if '=' in line and not line.strip().startswith('#'):
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())

FLUTTER_WEB_DIR = str(BASE_DIR / 'web_app')

app = Flask(__name__, static_folder=FLUTTER_WEB_DIR, static_url_path='')
CORS(app)

app.config['SECRET_KEY'] = os.environ.get('NEXUS_SECRET_KEY', 'nexus_omni_super_secret_key_2026')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///nexus_omni.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200), nullable=False)
    app_name = db.Column(db.String(200), nullable=False)
    user = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()
    run_auto_backup()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token = None
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1].strip()

        if not token:
            return jsonify({'error': 'رمز التحقق (Token) مفقود، يرجى تسجيل الدخول'}), 401

        try:
            data = serializer.loads(token, salt='nexus-auth', max_age=86400)
            current_user = data['username']
        except SignatureExpired:
            return jsonify({'error': 'انتهت صلاحية الجلسة، يرجى تسجيل الدخول مجدداً'}), 401
        except BadSignature:
            return jsonify({'error': 'رمز التحقق غير صالح'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/')
def serve_flutter_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'error': 'يرجى إدخال اسم المستخدم وكلمة المرور'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'اسم المستخدم موجود بالفعل'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'تم إنشاء الحساب بنجاح'}), 200

@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        token = serializer.dumps({'username': user.username}, salt='nexus-auth')
        return jsonify({
            'message': 'تم تسجيل الدخول بنجاح',
            'token': token,
            'username': user.username
        }), 200

    return jsonify({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}), 400

@app.route('/api/v1/records', methods=['GET'])
@token_required
def get_records(current_user):
    records = Record.query.filter_by(user=current_user).order_by(Record.id.desc()).all()
    records_list = [{
        'id': r.id,
        'action': r.action,
        'app': r.app_name,
        'user': r.user,
        'created_at': r.created_at
    } for r in records]
    return jsonify({'records': records_list}), 200

@app.route('/api/v1/data', methods=['POST'])
@token_required
def save_record(current_user):
    data = request.get_json()
    action = data.get('action', '').strip()
    app_name = data.get('app', '').strip()

    if not action or not app_name:
        return jsonify({'error': 'بيانات غير مكتملة'}), 400

    new_record = Record(
        action=action,
        app_name=app_name,
        user=current_user,
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    db.session.add(new_record)
    db.session.commit()

    return jsonify({'message': 'تم الحفظ بنجاح في السحابة المحلية'}), 200

@app.route('/api/v1/data/<int:record_id>', methods=['PUT'])
@token_required
def update_record(current_user, record_id):
    record = Record.query.filter_by(id=record_id, user=current_user).first()
    if not record:
        return jsonify({'error': 'السجل غير موجود أو غير مصرح بتعديله'}), 404

    data = request.get_json()
    action = data.get('action', '').strip()
    app_name = data.get('app', '').strip()

    if not action or not app_name:
        return jsonify({'error': 'يرجى إدخال اسم الإجراء والتطبيق'}), 400

    record.action = action
    record.app_name = app_name
    db.session.commit()

    return jsonify({'message': 'تم تعديل السجل بنجاح'}), 200

@app.route('/api/v1/data/<int:record_id>', methods=['DELETE'])
@token_required
def delete_record(current_user, record_id):
    record = Record.query.filter_by(id=record_id, user=current_user).first()
    if record:
        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': 'تم الحذف بنجاح'}), 200

    return jsonify({'error': 'السجل غير موجود أو غير مصرح بحذفه'}), 404

@app.route('/api/v1/data/clear', methods=['DELETE'])
@token_required
def clear_user_records(current_user):
    try:
        deleted_count = Record.query.filter_by(user=current_user).delete()
        db.session.commit()
        return jsonify({
            'message': f'تم حذف جميع سجلاتك بنجاح ({deleted_count} سجل)',
            'deleted': deleted_count
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'حدث خطأ أثناء المسح: {str(e)}'}), 500

@app.route('/api/v1/export', methods=['GET'])
@token_required
def export_data(current_user):
    records = Record.query.filter_by(user=current_user).all()
    records_list = [{
        'id': r.id,
        'action': r.action,
        'app': r.app_name,
        'user': r.user,
        'created_at': r.created_at
    } for r in records]

    buffer = io.BytesIO()
    buffer.write(json.dumps(records_list, ensure_ascii=False, indent=4).encode('utf-8'))
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'nexus_omni_{current_user}_backup.json',
        mimetype='application/json'
    )

@app.route('/api/v1/export/csv', methods=['GET'])
@token_required
def export_csv(current_user):
    records = Record.query.filter_by(user=current_user).order_by(Record.id.asc()).all()

    output = io.StringIO()
    output.write('\ufeff')
    writer = csv.writer(output)
    writer.writerow(['رقم السجل (ID)', 'الإجراء (Action)', 'التطبيق (App)', 'المستخدم (User)', 'تاريخ الإنشاء (Created At)'])

    for r in records:
        writer.writerow([r.id, r.action, r.app_name, r.user, r.created_at])

    buffer = io.BytesIO()
    buffer.write(output.getvalue().encode('utf-8'))
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'nexus_omni_{current_user}_report.csv',
        mimetype='text/csv; charset=utf-8'
    )

@app.route('/api/v1/import', methods=['POST'])
@token_required
def import_data(current_user):
    records_to_import = []

    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'لم يتم اختيار أي ملف'}), 400
        try:
            content = file.read().decode('utf-8')
            records_to_import = json.loads(content)
        except Exception:
            return jsonify({'error': 'ملف النسخة الاحتياطية غير صالح أو تالف'}), 400
    elif request.is_json:
        data = request.get_json()
        records_to_import = data.get('records', data) if isinstance(data, dict) else data
    else:
        return jsonify({'error': 'يرجى إرسال ملف JSON صالح'}), 400

    if not isinstance(records_to_import, list):
        return jsonify({'error': 'تنسيق البيانات غير صحيح'}), 400

    imported_count = 0
    skipped_count = 0

    try:
        for item in records_to_import:
            if not isinstance(item, dict):
                continue

            action = str(item.get('action', '')).strip()
            app_name = str(item.get('app', '')).strip()
            created_at = str(item.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))).strip()

            if not action or not app_name:
                continue

            exists = Record.query.filter_by(
                action=action,
                app_name=app_name,
                user=current_user,
                created_at=created_at
            ).first()

            if exists:
                skipped_count += 1
                continue

            new_record = Record(
                action=action,
                app_name=app_name,
                user=current_user,
                created_at=created_at
            )
            db.session.add(new_record)
            imported_count += 1

        db.session.commit()

        return jsonify({
            'message': f'تمت الاستعادة بنجاح: {imported_count} سجل جديد (تم تخطي {skipped_count} مكرر)',
            'imported': imported_count,
            'skipped': skipped_count
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'حدث خطأ أثناء حفظ البيانات: {str(e)}'}), 500

if __name__ == '__main__':
    print('Nexus Omni Production Server running on http://127.0.0.1:5000')
    serve(app, host='127.0.0.1', port=5000)
