import datetime
import json
import jwt
from blog import app, mongo
from blog.decorators import token_required
from blog.users.models import User
from flask import request, jsonify
from werkzeug.security import check_password_hash


@app.route('/user/register', methods=['POST'])
def user_register():
		data = json.loads(request.get_json())
		user = User(data)
		return user.create()

@app.route('/user/login', methods=['POST'])
def user_login():
		data = json.loads(request.get_json())
		username = data.get('username', None)
		password = data.get('password', None)
		if username != None and password != None:
				user = mongo.db.user.find_one({'username': username})
				if user == None or not check_password_hash(user['password'], password):
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
					})
		return jsonify({
				'error': 'Please, provide username and password!'
			})