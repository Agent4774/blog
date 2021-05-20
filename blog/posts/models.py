from datetime import datetime
import secrets
from flask import jsonify
from blog import mongo


class Post:
		def __init__(self, data):
				self.data = data

		def validate(self, data):
				title = data.get('title')
				content = data.get('content')
				if title == '' or content == '':
						return {'Alert!': 'Please provide title and content'}
				if len(title) > 100:
						return {'Alert!': 'Title must be of no more than 100 symbols!'}
				return True


		def create(self):
				validated = self.validate(self.data)
				if validated == True:
						post = {
							'title': self.data['title'],
							'content': self.data['content'],
							'created': datetime.utcnow(),
							'author': self.data['username']
						}
						mongo.db.post.insert_one(post)
						mongo.db.user.update_one(
							{'username': self.data['username']},
							{'$push': {'posts': post['_id']}}
						)
						del post['_id']
						return jsonify(post), 201
				return jsonify(validated), 400