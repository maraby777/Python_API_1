import json.decoder

from requests import Response

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookie, f"Cannot find cookie with name {cookie_name} in last response"
        return response.cookie[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header {headers_name} in last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        # Verify that response is JSON
        try:
            response_as_dist = response.json()
        except json.decoder.JSONDecoderError:
            assert False, f"Response is not in JSON format. Response text is in '{response.text}'"

        # Verify that name exists in returned response
        assert name in response_as_dist, f"Response JSON doesn't have any key '{name}'"
