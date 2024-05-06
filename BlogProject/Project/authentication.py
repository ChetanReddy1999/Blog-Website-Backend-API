import jwt
import datetime
from pymongo import MongoClient
from Project import constants
from bson import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash


# MongoDB configuration
mongo_client = MongoClient(constants.DEFAULT_MONGO_URL)
db = mongo_client[constants.MONGO_DATABASE]
collection = db[constants.USERS_COLLECTION]
blogs_collection = db[constants.BLOGS_COLLECTION]

# Function for User signUp
def signup(request):
    try:
        if 'username' not in request.form or 'password' not in request.form:
            return jsonify({'error':'SignUp unsuccessful!! Please provide username and password'}),400
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        existing_user = collection.find_one({'username':username})
        if existing_user is not None:
            return jsonify({'message':'Username already exists! Please choose a different one.'}),200

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Create new user and insert into db.
        result = collection.insert_one({'username':username,'password':hashed_password})
        if result.inserted_id is not None:
            return jsonify({'message':'SignUp successful!! Please login'}),201
        
        return jsonify({'error':'SignUp unsuccessful!! Please try again'}),400
    except Exception as e:
        return jsonify({'error': 'Error occured while Signing up '+str(e)}), 400

# JWT token generation function
def generate_token(username):
    token = jwt.encode({'username': username, 'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)}, constants.SECRET_KEY,algorithm="HS256")
    return token

# JWT token verification decorator
def token_required(f):
    def wrapper(*args,**kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({'error': 'Authorization header missing!!'}), 401
        token = request.headers.get('Authorization').strip(' ').split(' ')[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, constants.SECRET_KEY, algorithms="HS256")
            current_user = data['username']
            result = collection.find_one({'username':current_user})
            if result is None:
                return jsonify({'error': 'Token is invalid'}), 401
        except:
            return jsonify({'error': 'Token is invalid'}), 401

        return f(*args,**kwargs)

    return wrapper

# Function to check if user is authorized to make a particular API call
def is_authorized(f):
    def auth_wrapper(*args,**kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({'error': 'Authorization header missing!!'}), 401
        
        token = request.headers.get('Authorization').strip(' ').split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, constants.SECRET_KEY, algorithms="HS256")
            current_user = data['username']
            result = check_if_present_in_db(blog_id=args[1])
            if result is None or result['author_username']!=current_user:
                return jsonify({'message': 'User is not authorized'}), 401
        except:
            return jsonify({'error': 'Token is invalid'}), 401

        return f(*args,**kwargs)

    return auth_wrapper

# Function for User login
def login(request):
    try:
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({'message': 'Could not verify, please try again with your username and password'}), 401
        
        result = collection.find_one({'username':auth.username})

        if result and check_if_password_isequal(result,auth):
            token = generate_token(auth.username)
            return jsonify({'message':'Login Successful','token': token}),200

        return jsonify({'message': 'Could not verify, please try again with your username and password'}), 401
    except Exception as e:
        return jsonify({'error': 'Error occured while logging in '+str(e)}), 400
    
def check_if_password_isequal(result,auth):
    return check_password_hash(result['password'],auth.password)

def check_if_present_in_db(blog_id):
    return blogs_collection.find_one({'_id':ObjectId(blog_id)})
