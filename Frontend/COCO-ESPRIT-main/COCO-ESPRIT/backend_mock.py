"""
Mock Backend Server for COCO-ESPRIT
Simulates the Java Spring Boot backend on port 9092
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
CORS(app, supports_credentials=True, origins='http://localhost:4200')

# Secret key for JWT
SECRET_KEY = 'coco-esprit-secret-key'

# Mock database
users_db = {
    'admin': {
        'id': 1,
        'username': 'admin',
        'password': 'admin123',
        'email': 'admin@esprit.tn',
        'roles': ['ROLE_ADMIN', 'ROLE_USER']
    },
    'user': {
        'id': 2,
        'username': 'user',
        'password': 'user123',
        'email': 'user@esprit.tn',
        'roles': ['ROLE_USER']
    }
}

# Mock data
announcements = []
posts = []
houses = []

# Authentication endpoints
@app.route('/api/auth/signin', methods=['POST'])
def signin():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = users_db.get(username)
    
    if user and user['password'] == password:
        # Generate JWT token
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'roles': user['roles'],
            'accessToken': token,
            'tokenType': 'Bearer'
        }), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if username in users_db:
        return jsonify({'message': 'Username already exists'}), 400
    
    new_user = {
        'id': len(users_db) + 1,
        'username': username,
        'password': password,
        'email': email,
        'roles': ['ROLE_USER']
    }
    
    users_db[username] = new_user
    
    return jsonify({'message': 'User registered successfully'}), 200

# User endpoints
@app.route('/api/user/all', methods=['GET'])
def get_all_users():
    return jsonify([{
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'roles': user['roles']
    } for user in users_db.values()]), 200

@app.route('/api/user/retrieve/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users_db.values():
        if user['id'] == user_id:
            return jsonify({
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'roles': user['roles']
            }), 200
    return jsonify({'message': 'User not found'}), 404

# Carpooling endpoints
@app.route('/api/CarpoolingAnnouncement', methods=['GET'])
def get_carpooling_announcements():
    return jsonify(announcements), 200

@app.route('/api/CarpoolingAnnouncement', methods=['POST'])
def create_carpooling_announcement():
    data = request.json
    announcement = {
        'id': len(announcements) + 1,
        **data
    }
    announcements.append(announcement)
    return jsonify(announcement), 201

# Post/Forum endpoints
@app.route('/api/Post/retrieveAllPost', methods=['GET'])
def get_all_posts():
    return jsonify(posts), 200

@app.route('/api/Post/AddWithoutBadWord', methods=['POST'])
def create_post():
    data = request.json
    post = {
        'id': len(posts) + 1,
        **data,
        'createdAt': datetime.datetime.now().isoformat()
    }
    posts.append(post)
    return jsonify(post), 201

# House/Collocation endpoints
@app.route('/api/House/retrieveAllHouse', methods=['GET'])
def get_all_houses():
    return jsonify(houses), 200

@app.route('/api/House/addHouse', methods=['POST'])
def create_house():
    data = request.json
    house = {
        'id': len(houses) + 1,
        **data
    }
    houses.append(house)
    return jsonify(house), 201

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Mock Backend Server is running',
        'port': 9092
    }), 200

# Collocation announcement endpoints
@app.route('/api/AnnouncementCollocation/retrieveAllAnnouncement', methods=['GET'])
def get_collocation_announcements():
    return jsonify([]), 200

# Route endpoints
@app.route('/api/Route', methods=['GET'])
def get_routes():
    return jsonify([]), 200

# Car/Health endpoints
@app.route('/api/Health/retrieveAllCar', methods=['GET'])
def get_all_cars():
    return jsonify([]), 200

@app.route('/api/Health/addCar', methods=['POST'])
def add_car():
    data = request.json
    return jsonify({'id': 1, **data}), 201

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 COCO-ESPRIT Mock Backend Server")
    print("=" * 60)
    print("Server running on: http://localhost:9092")
    print("")
    print("📝 Test Accounts:")
    print("   Admin: username='admin', password='admin123'")
    print("   User:  username='user', password='user123'")
    print("=" * 60)
    app.run(debug=True, port=9092)
