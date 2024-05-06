
from Project import service,authentication
from flask import Flask, request
app = Flask(__name__)

# API to create a new blog
@app.route('/createblog', methods=['POST'])
def createblog():
    return service.create_blog(request)


# API to delete a blog by id
@app.route('/deleteblog/<string:blog_id>', methods=['DELETE'])
def delete(blog_id):
    return service.delete_blog(request,blog_id)


# API to list a specific blog
@app.route('/listblog', methods=['GET'])
@app.route('/listblog/<string:blog_id>', methods=['GET'])
def list_blog(blog_id=None):
    return service.list_blogs(request, blog_id)

# API to update blog
@app.route('/update/<string:blog_id>',methods=['PATCH'])
# @token_required
def update(blog_id):
    return service.update_blog(request,blog_id)


# SignUp API
@app.route('/signup', methods=['POST'])
def user_registration():
    return authentication.signup(request)

# Login API
@app.route('/login', methods=['POST'])
def user_login():
    return authentication.login(request)

    