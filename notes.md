##API Course:
### Parsing error

```python
# If the response is not valid JSON format, catch the parsing error
from json.decoder import JSONDecodeError
import requests

response = requests.get("https://playground.learnqa.ru/api/get_text")

# Attempt to parse the response body as JSON
try:
    parsed_response_text = response.json()
    print(parsed_response_text)
except JSONDecodeError:
    print(f"Response is not a JSON format.\nRaw response text: {response.text}\nStatus code: {response.status_code}")
```
_______________________________
### Sending different requests types (*17)

```python
import requests

requested_URL = "https://playground.learnqa.ru/api/check_type"
# All requests (exept GET) have request's body.  As second param in get request "params=" is passed,
# in another requests "data=" is passed
response_get = requests.get(requested_URL, params={"param1":"value1"})
print("GET: ", response_get.text)

response_post = requests.post(requested_URL, data={"param2":"POST"})
print("POST: ", response_post.text)

response_delete = requests.delete(requested_URL, data={"param3":"DELETE"})
print("DELETE: ", response_delete.text)

response_put = requests.put(requested_URL, data={"param4":"PUT"})
print("PUT: ", response_put.text)
```
---
## Status codes
https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status#informational_responses

HTTP response status codes indicate whether a specific HTTP request has been successfully completed. 

**Responses are grouped in five classes:**

- Informational responses (100 – 199)
- Successful responses (200 – 299)
- Redirection messages (300 – 399)
- Client error responses (400 – 499)
- Server error responses (500 – 599)
```python
import requests
from pprint import pprint # pprint = pretty print for visualisation of dicts, lists, JSON's, etc.

## Status Codes
# 301 Moved Permanently without following redirect (FALSE)
response = requests.get("https://playground.learnqa.ru/api/get_301", allow_redirects=False)
print("Status code without redirect:", response.status_code)

# 301 Moved Permanently with following redirect (TRUE)
response2 = requests.get("https://playground.learnqa.ru/api/get_301", allow_redirects=True)

#Save redirect steps
first_response = response2.history[0] #track redirection
second_response = response2
print(response2.status_code)

# Optional: print internal response data for debugging
#pprint(response2.__dict__)  # __dict__ spesial atrybute which consists all object's datas as dictionary
print(first_response.url)
print(second_response.url)
```

## Headers (*19)

```python
import requests

# HTTP = URL + headers + request body
# Header is additional info send with request
# More info about headers:  https://developer.mozilla.org/en-US/docs/Web/HTTP/

# Add custom header to request
headers = {"some_headers":"123"}
response = requests.get("https://playground.learnqa.ru/api/show_all_headers", headers = headers)

print(response.text)  # response from server (response body)
print(response.headers)  # meta data or dictionary with headers from server
```

## 🍪 Cookies (*20)
Coockies are small pices of data stored on client side (in browser).
 **Used to:**
- remember user session (stayed logged in)
- track user activity (analytics, ads)
- save preferences (language, region, theme, ...)

Sent by server via `Set-Cookie` header and automatically includes by the browser in the next request via `Cookie` header

###🧪 QA Use Cases for Cookies
Test login/logout flow.

- Check expiration (max-age, expires).

- Verify cookie flags (HttpOnly, Secure).

- Test cross-origin behavior (e.g. blocked by SameSite).

- Ensure proper cleanup after logout (cookie deleted/expired).

###Type of cookies:
**Session cookies** - temporary, deleted, when browser is closed
**Persistent** - have expiration and survive browser close
**HttpOnly** - cannot accessed by JavaScript (security)
**Secure** - sent over HTTPS
**SameSite** - control cross-site behavior (CORS-related)

```python
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

```
# Nagłówek 1
## Nagłówek 2
- Lista punktowana
- Kolejny punkt

**Pogrubienie**, *kursywa*, `kod w linii`

```python 
def hello(): print("Hello, world!") ``` 