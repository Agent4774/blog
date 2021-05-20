import datetime
import json
import secrets
from blog import app, mongo
from blog.decorators import token_required
from blog.posts.models import Post
from bson.objectid import ObjectId
from flask import request, jsonify


@app.route('/post/create', methods=['POST'])
@token_required
def create_post(current_user):
		data = json.loads(request.get_json())
		data['username'] = current_user['username']
		post = Post(data)
		return post.create()

@app.route('/post/<_id>', methods=['GET'])
@token_required
def retrieve_post(_, _id):
		post = mongo.db.post.find_one(
			{'_id': ObjectId(_id)}, 
			{'_id': 0}
		)
		return jsonify(post), 200

@app.route('/post/update/<_id>', methods=['PUT'])
@token_required
def update_post(_, _id):
		data = json.loads(request.get_json())
		mongo.db.post.update_one(
			{'_id': ObjectId(_id)},
			{'$set': data}
		)
		post = mongo.db.post.find_one(
			{'_id': ObjectId(_id)},
			{'_id': 0}
		)
		return jsonify(post), 200

@app.route('/post/delete/<_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, _id):
		# Deleting post itself
		mongo.db.post.delete_one(
			{'_id': ObjectId(_id)}
		)
		# Deleting post's public id from user posts array
		mongo.db.user.update_one(
			{'public_id': current_user['public_id']},
			{'$pull': {'posts': ObjectId(_id)}}
		)
		return jsonify({'detail': 'Post has been deleted!'}), 200