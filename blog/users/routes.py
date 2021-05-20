import datetime
import json
import jwt
from blog import app, mongo
from blog.decorators import token_required
from blog.users.models import User
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/user/register', methods=['POST'])
def user_register():
		data = json.loads(request.get_json())
		user = User(data)
		return user.create()

@app.route('/user/login', methods=['POST'])
def user_login():
		data = json.loads(request.get_json())
		username = data.get('username')
		password = data.get('password')
		if not username or not password:
				return jsonify({
					'error': 'Please, provide username and password!'
				}), 400
		user = mongo.db.user.find_one({'username': username})
		if not user or not check_password_hash(user['password'], password):
				return jsonify({
						'error': 'Invalid username or password!'
					}), 400
		payload = {
			'public_id': user['public_id'], 
			'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
		}
		token = jwt.encode(payload, app.config['SECRET_KEY'])
		return jsonify({
				'token': token
			}), 200

@app.route('/user/change-password', methods=['POST'])
@token_required
def change_password(current_user):
		data = json.loads(request.get_json())
		old_password = data.get('old_password')
		new_password = data.get('new_password')
		if not old_password or not new_password:
				return jsonify({'detail': 'Old password and new password required!'}), 400
		user = mongo.db.user.find_one(
				{'public_id': current_user['public_id']}
			)
		if not check_password_hash(user['password'], old_password):
				return jsonify({'detail': 'Wrong old password'}), 400
		mongo.db.user.update_one(
				{'public_id': current_user['public_id']},
				{'$set': {'password': generate_password_hash(new_password)}}
			)
		return jsonify({'detail': 'Password has been changed!'}), 200