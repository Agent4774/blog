import uuid
from blog import mongo
from flask import jsonify
from werkzeug.security import generate_password_hash


class User:
		def __init__(self, data):
				self.data = data

		def validate(self, data):
				#Username validation
				username = data.get('username')
				if username:						
						if mongo.db.user.find_one({'username': data['username']}):
								# If username exists
								return {'detail': 'Username already in use!'}
				else:
						return {'detail': 'Username required!'}
				# Email validation
				email = data.get('email')
				if email:
						if mongo.db.user.find_one({'email': data['email']}):
								# If email exists
								return {'detail': 'Email already in use!'}
						if '@' not in email or '.' not in email:
								# If correct email format
								return {'detail': 'Invalid email format!'}
				else:
						return {'detail': 'Email required!'}
				# Passwords validation
				password = data.get('password')
				password2 = data.get('password2')
				if password and password2:
						# if passwords don't match
						if password != password2:
								return {'detail': 'Passwords must match!'}
				else:
						return {'detail': 'password and password2 required!'}
				return True

		def create(self):
				validate = self.validate(self.data)
				if validate == True:
						# On valid data, add user to database
						user = {
							'public_id': uuid.uuid4().hex,
							'username': self.data['username'],
							'email': self.data['email'],
							'password': generate_password_hash(self.data['password']),
							'posts': []
						}						
						mongo.db.user.insert_one(user)
						# Removing unnecessary data
						del user['_id']
						del user['password']
						return jsonify(user), 201
				return jsonify(validate), 400