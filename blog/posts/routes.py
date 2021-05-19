import datetime
import json
import secrets
from blog import app, mongo
from blog.decorators import token_required
from blog.posts.models import Post
from flask import request, jsonify


@app.route('/post/create', methods=['POST'])
@token_required
def create_post(current_user):
		data = json.loads(request.get_json())
		post = Post(data)
		return post.create()
		

@app.route('/post/<public_id>', methods=['GET'])
@token_required
def retrieve_post(public_id):
		post = mongo.db.post.find_one({
				'public_id': public_id
			})
		return jsonify(post), 200

@app.route('/post/update/<public_id>', methods=['PUT'])
@token_required
def update_post(current_user, public_id):
		data = json.loads(request.get_json())
		mongo.db.post.update_one(
			{'public_id': public_id},
			{'$set': data}
		)
		return jsonify({'detail': 'Article has been updated!'}), 200

@app.route('/post/delete/<public_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, public_id):
		# delete post's public_id from user's posts array
		mongo.db.post.delete_one(
			{'public_id': public_id}
		)
		return jsonify({'detail': 'Article has been deleted!'}), 200