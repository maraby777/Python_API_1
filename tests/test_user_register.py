import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
from lib.my_requests import MyRequests

class TestUserRegister(BaseCase):

     def test_careate_new_user_successfully(self):
          params = self.prepare_registration_data()

          # Send POST request to register user
          response = MyRequests.post("/user/", data=params)

          # Assert correct status code and content
          Assertions.assert_code_status(response, 200)
          Assertions.assert_json_has_key(response, "id")

     def test_create_user_with_existing_mail(self):
          # Try to register with email that already exists
          email = 'vinkotov@example.com'
          params = self.prepare_registration_data(email)

          #Send POST request to register user
          response = MyRequests.post("/user/", data=params)

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

