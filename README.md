# Blog Website Backend API

- This repository contains backend APIs of a Blog website.
- APIs like create blog, delete blog,list blogs, update blog etc.. were implemented.
- MongoDB is used as Database to store relevant data.
- Authentication and authorization mechanisms were implemented as well.


## Database Architecture
   MongoDB consists of two collections. i) Users collection and ii) Blog collection
   <img width="718" alt="image" src="https://github.com/ChetanReddy1999/Blog_backend_API/assets/68106127/f7540beb-c235-4572-8ccd-7d01c5402d14">
   


## Requirements
1. User should install mongo
If User has docker enginer in their machine, they can directly run this command to initialize mongo server in your local.
```
docker run --name my-mongodb -d -p 27017:27017 mongo:latest
```
OR   follow mongod installation guide as mentioned in this link
[mongoDB istallation guide](https://www.mongodb.com/docs/manual/installation/#mongodb-installation-tutorials)

2. User should have Python interpretor with version 3.6+

## Setup Local Server
- Clone this repository.
- Run below command to install python packages
  ```
  pip install -r requirements.txt
  ```
- After installing packages run main.py file
  ```
  python main.py
  ```
- Flask server gets started in local with some port number.

# API Documentation:
**BaseUrl**: [http://localhost:<port_number>]()
### SignUp API:
API endpoint => [{{baseUrl}}/signup]()

Method => POST

cURL command
```
curl --location 'localhost:5000/signup' \
--form 'username="<enter username>"' \
--form 'password="<enter password>"'
```
Expected response
```
{
    "message": "SignUp successful!! Please login"
}
```

### Login API:
API endpoint => [{{baseUrl}}/login]()

Method => POST

cURL command
```
curl --location --request POST 'localhost:5000/login' \
--header 'Authorization: Basic <base64 encoded string>'
```
Encode your username:password into base64 in the website [base64encode](https://www.base64encode.org/)
and paste the encoded string in the above command and fire the API.
   
Eg: If your username is Charles and password is East@1234. Then encode the string **Charles:East@1234**, you'll get encode string as *Q2hhcmxlczpFYXN0QDEyMzQ=* and you can use the string in above curl command.

Expected response
```
{
    "message": "Login Successful",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFiYyIsImV4cCI6MTcxNDkyNzk0NX0.j2tjcdBIXwsFyrxk6k8Zjt-k0mAIUmAPKDnrBI2TPZU"
}
```
**Note** :- Above generate token is very important. That token is necessary to make subsequent calls.

### Create Blog API:
API endpoint => [{{baseUrl}}/createblog]()

Method => POST

cURL command
```
curl --location 'localhost:5000/createblog' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token generated from above login API>' \
--data '{
    "title":"<title of Blog>",
    "content":"<Blog content>",
    "author":"<author username>"
}'
```
1. Make sure you copy the token from Login API and paste in authorization header in the above curl command.
2. Populate data field with your desired blog title, content and author username.
3. Make sure you use the same username you used while logging in.
Expected response
```
{
    "message": "Blog created successfully"
}
```

### List Blog API:
API endpoint => [{{baseUrl}}/listblog]()

Method => GET

cURL command
```
curl --location 'localhost:5000/createblog' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token generated from above login API>' \
--data '{
    "title":"<title of Blog>",
    "content":"<Blog content>",
    "author":"<author username>"
}'
```
1. Make sure you copy the token from Login API and paste in authorization header in the above curl command.
2. Populate data field with your desired blog title, content and author username.
3. Make sure you use the same username you used while logging in.
Expected response
```
{
    "message": "Blog created successfully"
}
```

