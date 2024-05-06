
from uuid import uuid4

# change your mongo url accordingly
DEFAULT_MONGO_URL = 'mongodb://localhost:27017/'

MONGO_DATABASE = 'blog_db'

USERS_COLLECTION = 'users'

BLOGS_COLLECTION = 'blogs'

SECRET_KEY = str(uuid4().hex)
