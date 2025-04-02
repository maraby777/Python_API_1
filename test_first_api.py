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
