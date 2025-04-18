import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime

class TestUserRegister(BaseCase):
     def setup_method(self):
          # Generate a unique email address using timestamp
          base_part = 'learnqa'
          domain = 'example.com'
          random_part = datetime.now().strftime("%m%d%Y%H%M%S")
          self.email = f"{base_part}{random_part}@{domain}"

     def test_careate_new_user_successfully(self):

          params = {
               'password':'123',
               'username': 'learnqa',
               'firstName': 'learnqa',
               'lastName': 'learnqa',
               'email': self.email
          }
          # Send POST request to register user

          response = requests.post("https://playground.learnqa.ru/api/user/", data=params)

          # Assert correct status code and content
          Assertions.assert_code_status(response, 200)
          Assertions.assert_json_has_key(response, "id")

     def test_create_user_with_existing_mail(self):
          # Try to register with email that already exists
          email = 'vinkotov@example.com'
          params = {
               'password':'123',
               'username': 'learnqa',
               'firstName': 'learnqa',
               'lastName': 'learnqa',
               'email': email
          }

          #Send POST request to register user
          response = requests.post("https://playground.learnqa.ru/api/user/", data=params)

          # Assert correct status code and content
          Assertions.assert_code_status(response, 400)
          assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

          #assert response.content == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}" # Will fail
          # Actual response.content is: b"Users with email 'vinkotov@example.com' already exists",
          # b prefix means the left side is bytes that is compared to the right side which is str.
          # Check:
          #
          # print(type(response.content))  # -> tests\test_user_register.py <class 'bytes'>
          #
          # without decode to utf-8, expected string dosn't equel to actual result (str != bytes)
          # For formatinc content use: response.content.decode("utf-8")# or (if text content is always expected: response.text

