# Example for simple test run
# in terminal: python -m pytest test_examples.py -k "test_check_math"
# where "python -m  pytest" - runs pytest as python module ,
# test_examples.py - points to file with tests to run
# -k "test_check_math" - filters tests by name ( runt test which consists "test_check_math" in the name)
#                        To run exactly only one specific "test_check_math" and avoid substring matches,
#                        add '$' at the end: -k "test_check_math$"
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
        b = 10  # Intentional mismatch to trigger failure
        expected_sum = 14
        # Test will fail and print the custom message
        assert a+b == expected_sum, f"Sum of variables a and b is not equal to {expected_sum}"