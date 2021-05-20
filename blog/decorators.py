import jwt
from jwt.exceptions import DecodeError, InvalidSignatureError
from blog import app, mongo
from flask import jsonify, request
from functools import wraps


def token_required(f):
		@wraps(f)
		def wrap(*args, **kwargs):
				token = request.headers.get('x-access-token', None)
				if not token:
						return jsonify({'error': 'Please, provide a token!'}), 400
				try:
						data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
						current_user = mongo.db.user.find_one({
								'public_id': data['public_id']
							},
							{
								'_id': 0,
								'password': 0
							})
						return f(current_user, *args, **kwargs)
				except (DecodeError, InvalidSignatureError):
						return jsonify({'error': 'Invalid token!'}), 400
		return wrap