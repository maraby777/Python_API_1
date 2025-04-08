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