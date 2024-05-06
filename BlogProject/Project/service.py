'''
service.py have the functions that manipulate blogs in Database
'''
        
from datetime import datetime
from pytz import timezone
from flask import jsonify
from pymongo import MongoClient
from bson import ObjectId
from Project import constants
from Project.authentication import token_required,is_authorized

# MongoDB configuration
mongo_client = MongoClient(constants.DEFAULT_MONGO_URL)
db = mongo_client[constants.MONGO_DATABASE]
collection = db[constants.BLOGS_COLLECTION]


@token_required
def create_blog(request):
    try:
        data = request.json
        title = data.get('title')
        content = data.get('content')
        author = data.get('author')

        if not title or not content or not author:
            return jsonify({'error': 'Title and content are required'}), 400
        
        blog = {'title': title, 'content': content,'author_username':author,'created_at':datetime.now(timezone('Asia/Kolkata'))}
        result = collection.insert_one(blog)

        return jsonify({'message': 'Blog created successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'Error occured while creating blog '+str(e)}), 400

@is_authorized
def delete_blog(request,blog_id):
    result = collection.delete_one({'_id': ObjectId(blog_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Blog not found'}), 404

    return jsonify({'message': 'Blog deleted successfully'}), 200

@token_required
def list_blogs(request,blog_id):
    try:
        query = {}
        if blog_id is not None:
            query['_id'] = ObjectId(blog_id)
        else:
            author = request.args.get('author')
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')

            if author is not None:
                query['author'] = author

            if start_date is not None:
                query['created_at'] = {'$gte': datetime.strptime(start_date, '%Y-%m-%d')}

            if end_date is not None:
                if 'date' not in query:
                    query['created_at'] = {'$lte': datetime.strptime(end_date, '%Y-%m-%d')}
                else:
                    query['created_at']['$lte'] = datetime.strptime(end_date, '%Y-%m-%d')

        # Pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Calculate skip and limit for MongoDB query
        skip = (page - 1) * per_page
        limit = per_page


        posts = list(collection.find(query).skip(skip).limit(limit))
        for post in posts:
            post['_id'] = str(post['_id'])
        return posts,200
    
    except Exception as e:
        return jsonify({'error': 'Error occured while listing blogs '+str(e)}), 400
    
@is_authorized
def update_blog(request,blog_id):
    try:
        result = collection.find_one({'_id': ObjectId(blog_id)})
        if result is None:
            return jsonify({'error': 'Blog not found'}), 404
        title = result['title']
        content = result['content']
        data = request.json
        if 'title' in data:
            title = data['title']
        if 'content' in data:
            content = data['title']

        result = collection.update_one(
            {"_id": ObjectId(blog_id)},
            {'$set': 
                {
                    'title': title,
                    'content': content                    
                }
            },
            upsert=True
        )
        if result.modified_count == 1:
            return jsonify({'message': 'Blog updated successfully'}), 200
        
        return jsonify({'error': 'Blog not updated'}), 404
    except Exception as e:
        return jsonify({'error': 'Error occured while updating blog '+str(e)}), 400

        


        
        
        

