import pytest
import requests
# Test run in terminal: python -m pytest test_first_api.py
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
