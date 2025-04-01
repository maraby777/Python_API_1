import requests

# Cookies (
# --- Auth with valid credentials and cookies ---
# Prepare valid data and send request to receive auth cookies
payload = {"login":"secret_login", "password":"secret_pass"}
response1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)

print(response1.text)
print(response1.status_code)
print(dict(response1.cookies)) # cookie is an object, dict( set object as dictionary

# Store cookie and pass it to the second request
cookie_value = response1.cookies.get('auth_cookie')

cookies = {}                        # create dict
if cookie_value is not None:        # set cookie only if exists
    cookies.update({"auth_cookie": cookie_value})

# Second request with cookie tho check if we are authenticated
response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)

print("Second responce: ", response2.text)  # print: Second responce:  You are authorized

# --- Auth with invalid credentials ---
# Prepare invalid data  `1  1
payload2 = {"login":"secret_login", "password":"secret_pass2"}
response = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload2)

print(response.text)            # print: {"error":"Wrong data"}
print(response.status_code)     # Status code should be 200, the error with authorization is handled
print(dict(response.cookies))   # print: {}
