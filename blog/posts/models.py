import secrets
from flask import jsonify
from blog import mongo


class Post:
		def __init__(self, data):
				self.data = data

		def validate(self, data):
				title = data.get('title', None)
				content = data.get('content', None)
				if title == None or content == None:
						return {'Alert!': 'Please provide title and content'}
				if len(title) > 100:
						return {'Alert!': 'Title must be of no more than 100 symbols!'}
				return True


		def create(self):
				validated = self.validate(self.data)
				if validated == True:
					post = mongo.db.post.insert_one({
						'public_id': secrets.token_hex(8),
						'title': self.data['title'],
						'content': self.data['content'],
						'created': datetime.datetime.now(),
						'author': current_user['username']
					})
					post = mongo.db.post.find_one({'_id': post.inserted_id})
					mongo.db.user.update_one(
						{'public_id': current_user['public_id']},
						{'$push': {'posts': post['public_id']}}
					)
					return jsonify({'detail': 'Post has been created!'}), 201
				return jsonify(validated), 400