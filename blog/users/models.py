import uuid
from blog import mongo
from flask import jsonify
from werkzeug.security import generate_password_hash


class User:
		def __init__(self, data):
				self.data = data

		def validate(self, data):
				if 'username' in data and data['password'] != None \
				and 'password2' in data and data['password2'] != None:
						if mongo.db.user.find_one({'username': data['username']}):
								# if username exists
								return {'error': 'Username already in use!'}
						if mongo.db.user.find_one({'email': data['email']}):
								# if email exists
								return {'error': 'Email already in use!'}
				else:
						# If both username and email not provided
						return jsonify({'error': 'Username and email required!'})
				if 'password' in data and data['password'] != None \
				and 'password2' in data and data['password2'] != None:
						# if passwords don't match
						if data['password2'] != data['password']:
								return {'error': 'Passwords must match!'}
				else:
						# if passwords not provided
						return {'error': 'Password and its confirmation required!'}
				return True

		def create(self):
				validate = self.validate(self.data)
				if validate == True:
						obj = {
							'public_id': uuid.uuid4().hex,
							'username': self.data['username'],
							'email': self.data['email'],
							'password': generate_password_hash(self.data['password'])
						}
						# on valid data, add user to database
						user = mongo.db.user.insert_one(obj)
						response_data = mongo.db.user.find_one(
							{'_id': user.inserted_id}, 
							{'_id': 0, 'password': 0, 'public_id': 0}
						)
						return jsonify(response_data), 201
				return jsonify(validate), 400