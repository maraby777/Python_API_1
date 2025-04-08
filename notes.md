##API Course:

<details><summary><b>Parsing error by JSONDecodeError</b></summary>

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

</details>

_______________________________

<details><summary><b>Sending different requests types (*17)</b></summary>

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

</details>

---
### Status codes (*18)
https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status#informational_responses

HTTP response status codes indicate whether a specific HTTP request has been successfully completed. 

**Responses are grouped in five classes:**

- Informational responses (100 – 199)
- Successful responses (200 – 299)
- Redirection messages (300 – 399)
- Client error responses (400 – 499)
- Server error responses (500 – 599)
<details><summary>Code</summary>

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
</details>

---
<details><summary><b>Headers (*19) is additional info send with request</b></summary>

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
</details>

---

### 🍪 Cookies (*20)
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
- **Session cookies** - temporary, deleted, when browser is closed
- **Persistent** - have expiration and survive browser close
- **HttpOnly** - cannot accessed by JavaScript (security)
- **Secure** - sent over HTTPS
- **SameSite** - control cross-site behavior (CORS-related)

<details><summary>🍪 Cookies - code </summary>

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

</details>

---
### First pytest tests (*21)
In terminal: `python -m pytest test_examples.py -k "test_check_math"`
where:
 - `python -m  pytest` - runs pytest as python module, 
 - `"test_examples.py"` - points to file with tests to run , 
 - `-k "test_check_math"` - filters tests by name ( runt test which consists "test_check_math" in the name)

To run exactly only one specific "test_check_math" and avoid substring matches, add `'$'` at the end: `-k "test_check_math$"`

<details><summary>Code </summary>

```python
# Example for simple test run
class TestExample:
    # Valid test: this test should pass
    def test_check_math(self):
        a = 5
        b = 9
        expected_sum = 14
        # Asserts that a+b equals the expect sum , with thw custom message on failure
        assert a+b == expected_sum, f"Sum of variables a and b is not equal to {expected_sum}"

    # Failing test: this test will expect to fail due to incorrect sum
    def test_check_math2(self):
        a = 5
        b = 10
        expected_sum = 14
        # Test will fail and print the custom message
        assert a+b == expected_sum, f"Sum of variables a and b is not equal to {expected_sum}"
```
**Output:**

![](https://github.com/maraby777/Python_API_1/blob/main/doc_cache/png/pytest_first_tests_les21.png)

</details>

---

<details><summary><b>First API test (*22)</b></summary>

```python
import requests
# Test run in terminal: python -m pytest test_first_api.py
class TestFirstAPI:
    def test_hello_call(self):
        url = "https://playground.learnqa.ru/api/hello"
        name = 'Nat'
        data = {'name':name}

        # Send request and store response to variable
        response = requests.get(url, params=data)

        # Validate HTTP status code
        assert response.status_code == 200, "Wrong response code"

        # Parse response body as json()
        response_dict = response.json()

        # Verify if key 'answer' exists in JSON body
        assert "answer" in response_dict, "There is no field answer' in the response"

        #  Prepare expected response and extract actual one
        expected_response_text = f"Hello, {name}"
        actual_response_text = response_dict["answer"]

        # Compare expected and actual text
        assert actual_response_text == expected_response_text, "Actual text in the response is not correct"

```

</details>

---
####🔍 Parameterization in Pytest (*23)

Parameterization in Pytests allows you to launch the same test function many times with different data sets (arguments). Thanks to this:
- You do not have to copy the test code for various input data,
- tests are more transparent and scalable,
- It is easier to analyze which test cases have not passed.

<details><summary><b> Code</b></summary>

```python
import pytest
import requests

# Test run in terminal: python -m pytest test_first_api.py
# To run: python -m pytest test_first_api.py
class TestFirstAPI:
    # List of elements to verify the /hello endpoint
    names = [
        ("Vitaliy"),
        ("Nat"),
        ("")        # Empty name should return a generic greeting
    ]

    @pytest.mark.parametrize('name', names)
    def test_hello_call(self, name):
        url = "https://playground.learnqa.ru/api/hello"
        params = {'name':name}  # Load data from tuples

        # Send request and store response to variable
        response = requests.get(url, params=params)

        # Validate HTTP status code
        assert response.status_code == 200, "Wrong response code"

        # Parse response body as json()
        response_dict = response.json()

        # Verify if key 'answer' exists in JSON body
        assert "answer" in response_dict, "There is no field answer' in the response"

        if len(name) == 0:
            expected_response_text = "Hello, someone"
        else:
            #  Prepare expected response and extract actual one
            expected_response_text = f"Hello, {name}"

        # After refactor:
        # expected_respose_text = f"Hello, {name}" if name else  "Hello, someone"

        actual_response_text = response_dict["answer"]
        print(f"Response for name={name}': {actual_response_text}") # Contextual print for debugging

        # Compare expected and actual text
        assert actual_response_text == expected_response_text, "Actual text in the response is not correct"
```
</details>

---

<details><summary><b>Auth tests (*24&*25)</b></summary>

```python
import requests
import pytest

class TestUserAuth:
    def test_user_auth(self):
        params = {
            'email':'vinkotov@example.com',
            'password':'1234'
        }

        # Send POST to log in
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=params)

        #Validate values in respose
        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "Tere is no CSRF token header in the response"
        assert "user_id" in response1.json(), "There is no user id in the response body"

        # Just debug :)
        print(response1.json())

        # Extract values for authorization
        auth_sid = response1.cookies.get("auth_sid")
        token = response1.headers.get("x-csrf-token")
        user_id_from_auth_method = response1.json()["user_id"]

        # Send GET to check user authorization
        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token":token},
            cookies={"auth_sid":auth_sid}
        )

        # Validate user_id in response
        assert "user_id" in response2.json(), "There is no user is in the response2 body"

        # Compare expected and actual user_id
        user_id_from_check_method = response2.json()["user_id"]
        print(f"Response2 {response2.json()}")

        assert user_id_from_auth_method == user_id_from_check_method, "User id from auth method is not equal to user id from check method"

##  Parameterized negative test: missing cookie or token
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        # Prepare login credentials
        params = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        # Send POST to log in
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=params)

        # Validate data in response
        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "Tere is no CSRF token header in the response"
        assert "user_id" in response1.json(), "There is no user id in the response body"

        # Debug info
        print(response1.json())

        # Extract value for authorization
        auth_sid = response1.cookies.get("auth_sid")
        token = response1.headers.get("x-csrf-token")

        # Choose what to exclude based on the test condition
        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token":token}
        ) if condition == "no_cookies" else requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            cookies={"auth_sid":auth_sid}
        )

        # Longer version
        # if condition == 'no_cookie':
        #     response2 = requests.get(
        #         "https://playground.learnqa.ru/api/user/auth",
        #         headers={"x-csrf-token":token}
        #     )
        # else:     # no_token
        #     response2 = requests.get(
        #         "https://playground.learnqa.ru/api/user/auth",
        #         cookies={"auth_sid":auth_sid}
        #     )


        # Validate that user is not authorized
        assert "user_id" in response1.json(), "There is no user id in the response2 body"
        user_id_from_check_method = response2.json()["user_id"]

        # Debug outprint
        print(f"Response2 _negative:  {response2.json()}")

        assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"

```

</details>

---

#### Setup_method(self, method) – classic “xUnit style” approach
This is a special method that is automatically executed before EVERY test method in the class.

🔧 **Usage:**
- You have to name it exactly setup_method(self, method) – pytest requires it.
- You can use teardown_method(self, method) if you want to clean up something after the test.

<details><summary><b>Code</b></summary>

```python
import requests
import pytest

## For run test use in terminal: python -m pytest test_user_auth.py -s

class TestUserAuth:
    ##  Parameterized negative test: missing cookie or token
    exclude_params = ["no_cookie", "no_token"]

    def setup_method(self, method):
        # Credential data
        params = {
            'email':'vinkotov@example.com',
            'password':'1234'
        }

        # Send POST to log in
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=params)

        #Validate values in respose
        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF token header in the response"
        assert "user_id" in response1.json(), "There is no user id in the response body"

        # Extract values for reuse in tests
        self.auth_sid = response1.cookies.get("auth_sid")
        self.token = response1.headers.get("x-csrf-token")
        self.user_id_from_auth_method = response1.json()["user_id"]


    def test_user_auth(self):
        # Send GET to check user authorization
        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token":self.token},
            cookies={"auth_sid":self.auth_sid}
        )

        # Validate user_id in response
        assert "user_id" in response2.json(), "There is no user is in the response2 body"

        # Compare expected and actual user_id
        user_id_from_check_method = response2.json()["user_id"]
        print(f"Response2 {response2.json()}")

        assert self.user_id_from_auth_method == user_id_from_check_method, "User id from auth method is not equal to user id from check method"

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        # Choose what to exclude based on the test condition
        response = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token":self.token}
        ) if condition == "no_cookies" else requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            cookies={"auth_sid":self.auth_sid}
        )

        # Longer version
        # if condition == 'no_cookie':
        #     response2 = requests.get(
        #         "https://playground.learnqa.ru/api/user/auth",
        #         headers={"x-csrf-token":self.token}
        #     )
        # else:     # no_token
        #     response2 = requests.get(
        #         "https://playground.learnqa.ru/api/user/auth",
        #         cookies={"auth_sid":self.auth_sid}
        #     )


        # Validate that user is not authorized
        assert "user_id" in response.json(), "There is no user id in the response2 body"
        user_id_from_check_method = response.json()["user_id"]

        # Debug outprint
        print(f"Response _negative test:  {response.json()}")

        assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"

```


# Nagłówek 1
## Nagłówek 2
- Lista punktowana
- Kolejny punkt

**Pogrubienie**, *kursywa*, `kod w linii`

```python 
def hello(): print("Hello, world!") ``` 