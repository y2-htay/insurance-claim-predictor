JWT Authentication with Djoser

1. To create user

Install POSTMAN extension on VSCODE/IDE
On POSTMAN set up a POST request to http://127.0.0.1:8001/api/auth/users 
Under ‘Body’ -> ‘form-data’ insert key: value pairs
"username": "example_username", "password": "example_password"
You should receive a response like:
{
    "id": 1,
    "username": "admin",
    "permission_level": 0
}

2. To obtain JWT token (login)

Set up a POST request to http://127.0.0.1:8001/api/auth/jwt/create/
Under ‘Body’ -> ‘form-data’ insert key: value pairs
"username": "example_username", "password": "example_password"
You should receive a response like:
"refresh": "your_refresh_token",
"access": "your_access_token"
This token will be used to access restricted endpoints

3. To test protected endpoint
Set up a GET request to http://127.0.0.1:8001/api/protected/
Try without any input data, see what response you get (not authenticated)
To gain access, go to headers tab insert key: value pair
"Authorization": "Bearer your_access_token" - SEND
You should receive:
{
    "message": "You have access to this protected endpoint! User: your_username"
}

