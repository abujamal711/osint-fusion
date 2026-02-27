from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, User, Search, AuditLog
from auth import generate_token, token_required
from utils import OSINTCollector
from config import Config
import json
from datetime import datetime

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.config.from_object(Config)
CORS(app)
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

collector = OSINTCollector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

# API Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401
    token = generate_token(user.id)
    # Log login
    log = AuditLog(user_id=user.id, action='LOGIN', details='User logged in', ip_address=request.remote_addr)
    db.session.add(log)
    db.session.commit()
    return jsonify({'token': token, 'username': user.username})

@app.route('/api/search', methods=['POST'])
@token_required
def search(current_user):
    data = request.json
    target = data.get('target')
    target_type = data.get('type')  # email, phone, username
    if not target or not target_type:
        return jsonify({'message': 'Target and type required'}), 400

    # Perform OSINT based on type
    if target_type == 'email':
        result = collector.check_email(target)
    elif target_type == 'phone':
        result = collector.check_phone(target)
    elif target_type == 'username':
        result = collector.check_username(target)
    else:
        return jsonify({'message': 'Invalid type'}), 400

    # Save search to DB
    search = Search(
        user_id=current_user.id,
        target=target,
        target_type=target_type,
        result=json.dumps(result),
        ip_address=request.remote_addr
    )
    db.session.add(search)

    # Audit log
    log = AuditLog(user_id=current_user.id, action='SEARCH', details=f'{target_type}: {target}', ip_address=request.remote_addr)
    db.session.add(log)
    db.session.commit()

    return jsonify({'result': result})

@app.route('/api/history', methods=['GET'])
@token_required
def history(current_user):
    searches = Search.query.filter_by(user_id=current_user.id).order_by(Search.timestamp.desc()).all()
    return jsonify([{
        'id': s.id,
        'target': s.target,
        'type': s.target_type,
        'timestamp': s.timestamp.isoformat(),
        'result': json.loads(s.result) if s.result else {}
    } for s in searches])

@app.route('/api/logs', methods=['GET'])
@token_required
def get_logs(current_user):
    if not current_user.is_admin:
        return jsonify({'message': 'Admin only'}), 403
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(100).all()
    return jsonify([{
        'user': log.user_id,
        'action': log.action,
        'details': log.details,
        'timestamp': log.timestamp.isoformat(),
        'ip': log.ip_address
    } for log in logs])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
