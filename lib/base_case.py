import json.decoder
from requests import Response
from datetime import datetime

class BaseCase:
    def get_cookie(self, response: Response, cookies_name):
        assert cookies_name in response.cookies, f"Cannot find cookie with name {cookies_name} in last response"
        return response.cookies[cookies_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header {headers_name} in last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        # Verify that response is JSON
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecoderError:
            assert False, f"Response is not in JSON format. Response text is in '{response.text}'"

        # Verify that name exists in returned response
        assert name in response_as_dict, f"Response JSON doesn't have any key '{name}'"
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"

        return{
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

