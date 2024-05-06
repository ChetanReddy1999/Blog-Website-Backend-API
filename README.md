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
**BaseUrl**: [http://localhost:<port_number>]()<br>
**Note** : A zip file with all the API data is provided in the repository, you can import that file in postman to test the APIs effortlessly.
### SignUp API:
API endpoint => [{{baseUrl}}/signup]()

Method => POST

**cURL command**
```
curl --location 'localhost:5000/signup' \
--form 'username="<enter username>"' \
--form 'password="<enter password>"'
```
**Through Postman**
```
- Open SignUp API in postman.
- You can change username and password in body's form-data.
```
<img width="1292" alt="image" src="https://github.com/ChetanReddy1999/Blog_backend_API/assets/68106127/dd0911a6-9cc8-4837-ab02-422379660493">

1. Other usecases like if username is already in use, will receive an error asking to change username.
2. If username or password not provided in the API, it will raise an error.

**Expected response**
```
{
    "message": "SignUp successful!! Please login"
}
```

### Login API:
API endpoint => [{{baseUrl}}/login]()

Method => POST

**cURL command**
```
curl --location --request POST 'localhost:5000/login' \
--header 'Authorization: Basic <base64 encoded string>'
```
Encode your username:password into base64 in the website [base64encode](https://www.base64encode.org/)
and paste the encoded string in the above command and fire the API.
   
Eg: If your username is Charles and password is East@1234. Then encode the string **Charles:East@1234**, you'll get encode string as *Q2hhcmxlczpFYXN0QDEyMzQ=* and you can use the string in above curl command.

**Through Postman**
```
- Open Login API in postman.
- You can add your username and password in Authorization tab as shown in below figure.
```
<img width="1289" alt="image" src="https://github.com/ChetanReddy1999/Blog_backend_API/assets/68106127/4271ca0d-3cf8-4e6f-9c70-955798bcd611">

1. Other usecases like wrong username, wrong password or API without username or password can be checked.

**Expected response**
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

**cURL command**
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
3. Make sure you use the same username in the author name in body you used while logging in.
   
**Through Postman**
```
- Open CreateBlog API in postman.
- Make sure you copy the token from Login API and paste in authorization header as Bearer token.
- You can add your content in the body as shown inthe below figure.
```
<img width="1302" alt="image" src="https://github.com/ChetanReddy1999/Blog_backend_API/assets/68106127/484d202b-071a-4144-ad84-2d800318665d">

**Expected response**
```
{
    "message": "Blog created successfully"
}
```

### List Blog API:
API endpoint => [{{baseUrl}}/listblog]()

Method => GET

**cURL command**
```
curl --location 'localhost:5000/listblog?start_date=2024-1-1&end_date=2024-5-3&page=1&per_page=2&author=Chetan' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFiYyIsImV4cCI6MTcxNDk0NzcwOH0.pqma2DnsYzKNUvaNfQG8G8f2FtfsnbPV5-z1GidOmSo'
```
1. Make sure you copy the token from Login API and paste in authorization header in the above curl command.
2. Populate queryparam fields with start data,end date in 'YYYY-MM-DD' format. You can also include page number, records per page,author query param.
3. Any queryparam is optional you can run API without giving queryparam which will result in listing all the blogs.

**Through Postman**
```
- Open List Blog API in postman.
- Make sure you copy the token from Login API and paste in authorization header as Bearer token.
- Add filters like author,start data, end date, elements per page, page number etc in query params as shown in the figure.
- If you want to list all the blogs you can uncheck all the queryparams like author,startdate etc..
```
<img width="1292" alt="image" src="https://github.com/ChetanReddy1999/Blog_backend_API/assets/68106127/ee9bccc5-fbc0-4e2b-b4b6-181142993f5e">


Expected response
```
{
    "message": "Blog created successfully"
}
```

