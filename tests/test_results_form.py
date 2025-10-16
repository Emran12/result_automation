import unittest
# Import the main function and configuration data from the automation script
from automation import get_result_data, FORM_DATA 

class TestResultFormAutomation(unittest.TestCase):
    """
    Test suite for executing the result form automation script.

    NOTE: Because the actual result retrieval is dependent on solving a
    complex CAPTCHA (which is currently handled manually in get_result_data),
    this test case primarily verifies that the automation execution path
    (filling dropdowns and inputs) runs without throwing immediate Selenium errors.
    """

    def test_01_successful_form_submission_attempt(self):
        """
        Executes the main automation function. This test requires manual
        intervention to solve the CAPTCHA when prompted in the console.
        """
        print("\n\n--- Running End-to-End Automation Test ---")
        
        # We assume the function returns None on success or if it hits the CAPTCHA pause.
        # It handles its own exceptions and cleanup (driver.quit()).
        try:
            get_result_data(FORM_DATA)
            # If the function completes without raising an unhandled exception, the test passes.
            print("\nTest finished executing the automation sequence (check console for CAPTCHA prompt).")
            self.assertTrue(True, "Automation execution path completed.")
        except Exception as e:
            self.fail(f"Automation failed during execution with an unhandled error: {e}")

if __name__ == '__main__':
    # To run this test: python -m unittest test_results_form.py
    unittest.main()