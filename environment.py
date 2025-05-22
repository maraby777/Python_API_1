import os
# Set in the Terminal: $env:ENV = 'prod'  / $env:ENV = 'dev'
# Check Variable: echo $env:ENV
class Environment:
    DEV = 'dev'
    PROD = 'prod'
    # Dictionary that maps 'dev' or 'prod' to specific URL
    URLS = {
        DEV: 'https://playground.learnqa.ru/api_dev',
        PROD: 'https://playground.learnqa.ru/api'
    }

    def __init__(self):
        try:
            # Read the value of the ENV environment variable
            self.env = os.environ['ENV']
        except KeyError:
            # Default env variable
            self.env = self.DEV

    # Returns URL matching the current environment or throws an error
    def get_base_url(self):
        if self.env in self.URLS:
            return self.URLS[self.env]
        else:
            raise Exception(f"Unknown value of ENV variable {self.env}")
# A global object that is used everywhere (after import), so it not need to create a new one every time
ENV_OBJECT = Environment()