# routes.py
from flask import Blueprint, request, jsonify
from .models import db, User, FamilyMember, Pregnancy
from flask_jwt_extended import create_access_token, jwt_required

routes = Blueprint('routes', __name__)

@routes.route('/signup', methods=['POST'])
def signup():
    data = request.json
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@routes.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    pregnancies = Pregnancy.query.filter_by(user_id=user.id).all()
    return jsonify({'pregnancies': [p.start_date for p in pregnancies]})

@routes.route('/emergency', methods=['POST'])
@jwt_required()
def emergency():
    user_id = get_jwt_identity()
    family_members = FamilyMember.query.filter_by(user_id=user_id).all()
    # Send alerts to family members (implementation depends on SMS service).
    return jsonify({'message': 'Emergency alert sent'})
