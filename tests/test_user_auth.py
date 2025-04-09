import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

## For run test use in terminal: python -m pytest tests/test_user_auth.py -s

class TestUserAuth(BaseCase):
    ##  Parameterized negative test: missing cookie or token
    exclude_params = ["no_cookie", "no_token"]

    def setup_method(self, method):
        # Credential data
        params = {
            'email':'vinkotov@example.com',
            'password':'1234'
        }

        # Perform login POST request
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=params)

        # Extract required authentication values using BaseCase helper methods
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        print("Login user_id:", self.user_id_from_auth_method)
        print("Check user_id:", response1.json())

    # Verify user_id from /auth  is the same as user_is from /login
    def test_user_auth(self):
        # Send GET to check if user still authorized using cookies and headers
        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        # Validate user_id in response
        Assertions.asser_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method")

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

        # Validate the user is NOT authorized
        Assertions.asser_json_value_by_name(
            response,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )

        ## Validate that user is not authorized
        ## assert "user_id" in response.json(), "There is no user id in the response2 body"  # -> moved to Assertions.asser_json_value_by_name()
        ##user_id_from_check_method = response.json()["user_id"]

        ## assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"  # -> moved to Assertions.asser_json_value_by_name()