from Project import routes,authentication,constants
from requests.auth import _basic_auth_str
import datetime,jwt
from bson import ObjectId
from pymongo.results import DeleteResult
from typing import Mapping

# Mocking MongoDB client and collection
class MockCollection:
    def __init__(self, data):
        self.data = data
    
    def find_one(self, query):
        # Simulating MongoDB find_one method
        return self.data
    
    def delete_one(self, query):
        # Simulating MongoDB delete_one method
        return {'deleted_count': 1}

class TestRoutes:
    def test_signup_successful(self,mocker):
        mocker.patch("pymongo.collection.Collection.find_one",return_value=None)

        response = routes.app.test_client().post('/signup',content_type='multipart/form-data',data = dict({'username':'abc','password':'abc'}))
        # Check if signup was successful
        assert response.status_code == 201


    def test_signup_unsuccessful(self,mocker):
        mocker.patch("pymongo.collection.Collection.find_one",return_value={'username':'abc','password':'abc'})

        response = routes.app.test_client().post('/signup',content_type='multipart/form-data',data = dict({'username':'abc','password':'abc'}))
        # Check if signup was unsuccessful
        assert response.status_code == 200

        response = routes.app.test_client().post('/signup',content_type='multipart/form-data',data = dict({'password':'abc'}))
        # Check if signup was unsuccessful
        assert response.status_code == 400


    def test_signup_mongoerror(self,mocker):
        mocker.patch("pymongo.collection.Collection.find_one",side_effect=Exception("new exception"))
        response = routes.app.test_client().post('/signup',content_type='multipart/form-data',data = dict({'username':'xyz','password':'abc'}))
        # Check if signup was unsuccessful
        assert response.status_code == 400
 
    def test_login_successful(self,mocker):
        mocker.patch("pymongo.collection.Collection.find_one",return_value={'username':'abc','password':'abc'})
        mocker.patch("Project.authentication.check_if_password_isequal",return_value=True)
        response = routes.app.test_client().post('/login',headers={"Authorization": _basic_auth_str('abc', 'abc')})
        # Check if signup was successful
        assert response.status_code == 200

    def test_login_unsuccessful(self,mocker):
        mocker.patch("pymongo.collection.Collection.find_one",return_value={'username':'abc','password':'abc'})
        response = routes.app.test_client().post('/login',headers={"unknown": _basic_auth_str('abc', 'abc')})
        # Check if signup was unsuccessful
        assert response.status_code == 401

        mocker.patch("Project.authentication.check_if_password_isequal",return_value=False)
        response = routes.app.test_client().post('/login',headers={"Authorization": _basic_auth_str('abc', 'abc')})
        assert response.status_code == 401

        mocker.patch("Project.authentication.check_if_password_isequal",side_effect=Exception("new excepton"))
        response = routes.app.test_client().post('/login',headers={"Authorization": _basic_auth_str('abc', 'abc')})
        assert response.status_code == 400


    # Testing create Blog API
    def test_createblog_successful(self,mocker):
        token = jwt.encode({'username': 'abc', 'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)}, constants.SECRET_KEY,algorithm="HS256")
        data = {"title":"Importance of Education","content":"Education is mandatory for everyone and it is a birth right","author":"abc"}
        response = routes.app.test_client().post('/createblog',json=data,headers={"Authorization": "Bearer "+token})
        assert response.status_code == 201

    def test_createblog_unsuccessful(self,mocker):
        token = jwt.encode({'username': 'abc', 'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)}, constants.SECRET_KEY,algorithm="HS256")
        data = {}
        response = routes.app.test_client().post('/createblog',json=data,headers={"Authorization": "Bearer "+token})
        assert response.status_code == 400

        data = {"title":"Importance of Education","content":"Education is mandatory for everyone and it is a birth right","author":"abc"}
        mocker.patch("pymongo.collection.Collection.insert_one",side_effect=Exception("new exception"))
        response = routes.app.test_client().post('/createblog',json=data,headers={"Authorization": "Bearer "+token})
        assert response.status_code == 400

    # Test List blogs API
    def test_listblog_successful(self,mocker):
        token = jwt.encode({'username': 'abc', 'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)}, constants.SECRET_KEY,algorithm="HS256")
        query = {'author':'abc','start_date':'2024-4-16','end_date':'2024-5-1'}
        response = routes.app.test_client().get('/listblog',query_string=query,headers={"Authorization": "Bearer "+token})
        assert response.status_code == 200

        response = routes.app.test_client().get('/listblog/'+str(ObjectId('aaaaaaaaaaaaaaaaaaaaaaaa')),headers={"Authorization": "Bearer "+token})
        assert response.status_code == 200

    def test_listblog_unsuccessful(self,mocker):
        token = jwt.encode({'username': 'abc', 'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)}, constants.SECRET_KEY,algorithm="HS256")
        query = {'author':'abc','start_date':'2024-4-16','end_date':'2024-5-1'}
        # mocker.patch("pymongo.collection.Collection.find",side_effect=Exception("new exception"))
        response = routes.app.test_client().get('/listblog',query_string=query,headers={"unknown": "Bearer "+token})
        assert response.status_code == 401

        mocker.patch("pymongo.collection.Collection.find_one",return_value=None)
        response = routes.app.test_client().get('/listblog',query_string=query,headers={"Authorization": "Bearer "+token})
        assert response.status_code == 401

        mocker.patch("pymongo.collection.Collection.find_one",side_effect=Exception("new exception"))
        response = routes.app.test_client().get('/listblog',query_string=query,headers={"Authorization": "Bearer "+token})
        assert response.status_code == 401


    # Test delete blog
    def test_deleteblog_unsuccessful(self,mocker):
        token = jwt.encode({'username': 'abc', 'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)}, constants.SECRET_KEY,algorithm="HS256")
        example_mapping: Mapping[str, int] = {'deleted_count': 1}
        mocker.patch("pymongo.collection.Collection.delete_one",return_value=DeleteResult(example_mapping,True))
        mocker.patch("Project.authentication.check_if_present_in_db",return_value={'author_username':'abc'})
        response = routes.app.test_client().delete('/deleteblog/'+str(ObjectId('aaaaaaaaaaaaaaaaaaaaaaaa')),headers={"Authorization": "Bearer "+token})
        assert response.status_code == 404

        mocker.patch("Project.authentication.check_if_present_in_db",return_value=None)
        response = routes.app.test_client().delete('/deleteblog/'+str(ObjectId('aaaaaaaaaaaaaaaaaaaaaaaa')),headers={"Authorization": "Bearer "+token})
        assert response.status_code == 401

        mocker.patch("Project.authentication.check_if_present_in_db",side_effect=Exception("new exception"))
        response = routes.app.test_client().delete('/deleteblog/'+str(ObjectId('aaaaaaaaaaaaaaaaaaaaaaaa')),headers={"Authorization": "Bearer "+token})
        assert response.status_code == 401
    

    # Test updateblog blog
    def test_updateblog_unsuccessful(self,mocker):
        token = jwt.encode({'username': 'abc', 'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)}, constants.SECRET_KEY,algorithm="HS256")
        mocker.patch("pymongo.collection.Collection.find_one",return_value={"title":"Importance of Education","content":"Education is mandatory for everyone and it is a birth right","author":"abc"})
        mocker.patch("Project.authentication.check_if_present_in_db",return_value={'author_username':'abc'})

        data = {"title":"Importance of Education","content":"Education is mandatory for everyone and it is a birth right","author":"abc"}
        response = routes.app.test_client().patch('/update/'+str(ObjectId('aaaaaaaaaaaaaaaaaaaaaaaa')),json=data,headers={"Authorization": "Bearer "+token})
        assert response.status_code == 404

        mocker.patch("pymongo.collection.Collection.find_one",side_effect=None)
        response = routes.app.test_client().patch('/update/'+str(ObjectId('aaaaaaaaaaaaaaaaaaaaaaaa')),json=data,headers={"Authorization": "Bearer "+token})
        assert response.status_code == 404

        mocker.patch("pymongo.collection.Collection.find_one",return_value={})
        response = routes.app.test_client().patch('/update/'+str(ObjectId('aaaaaaaaaaaaaaaaaaaaaaaa')),json=data,headers={"Authorization": "Bearer "+token})
        assert response.status_code == 400