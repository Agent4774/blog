import datetime
import json
import jwt
import secrets
from blog import app, mongo
from blog.decorators import token_required 
from blog.models import User
from flask import request, jsonify, session
from slugify import slugify
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

@app.route('/post/create', methods=['POST'])
@token_required
def create_post(current_user):
		data = json.loads(request.get_json())
		post = mongo.db.post.insert_one({
				'public_id': secrets.token_hex(8),
				'title': data['title'],
				'content': data['content'],
				'created': datetime.datetime.now(),
				'author': current_user['username']
			})
		post = mongo.db.post.find_one({'_id': post.inserted_id})
		mongo.db.user.update_one(
			{'public_id': current_user['public_id']},
			{'$push': {'posts': {'public_id': post['public_id']}}}
		)
		return jsonify({'detail': 'Post has been created!'})

@app.route('/post/update/<public_id>', methods=['PUT'])
@token_required
def update_post(current_user, public_id):
		data = json.loads(request.get_json())
		mongo.db.post.update_one(
			{'public_id': public_id},
			{'$set': data}
		)
		return jsonify({'detail': 'Article has been updated!'})

@app.route('/post/delete/<public_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, public_id):
		mongo.db.post.delete_one(
			{'public_id': public_id}
		)

		return jsonify({'detail': 'Article has been deleted!'})