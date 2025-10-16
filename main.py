import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from pages.results_page import ResultsPage

# --- CONFIGURATION ---
URL = "https://eboardresults.com/v2/home"  # <<< REPLACE with the actual result site URL
# DRIVER_PATH = 'path/to/chromedriver' # Uncomment if driver is not in PATH

# Sample data to fill the form (FORM_DATA is now defined here)
FORM_DATA = {
    "board": "madrasah",          
    "exam": "hsc", 
    "year": "2025",
    "result_type": "1",
    "roll_number": "166782",
    "reg_number": "1918637269",
}

# --- UTILITY: CAPTCHA SOLVING LOGIC ---

def solve_captcha_manual(page_object):
    """
    PAUSES the script and asks the human user to solve the CAPTCHA.
    
    @param page_object: An instance of ResultsPage.
    @return: The user-provided CAPTCHA solution string.
    """
    if page_object.save_captcha_image():
        print("\n--- ATTENTION REQUIRED ---")
        print("A screenshot of the CAPTCHA image has been saved as 'current_captcha.png'.")
        print("Please solve the CAPTCHA in the open browser window.")
        
        # Ask for manual input
        captcha_solution = input("Enter the CAPTCHA text: ")
        return captcha_solution.strip()
    return ""

# --- MAIN EXECUTION FUNCTION ---

def run_automation(data):
    """
    Initializes the driver and runs the automation sequence.
    """
    driver = None
    try:
        # Initialize the Chrome WebDriver
        if 'DRIVER_PATH' in locals() and os.path.exists(DRIVER_PATH):
            driver = webdriver.Chrome(service=ChromeService(executable_path=DRIVER_PATH))
        else:
            driver = webdriver.Chrome() # Assumes chromedriver is in system PATH

        driver.maximize_window()
        driver.get(URL)
        time.sleep(2)  # Wait for page load
        print(URL)
        # Instantiate the Page Object
        results_page = ResultsPage(driver)
        print("Starting form automation using POM structure...")

        # 1. Fill the form inputs
        results_page.fill_form_data(data)
        print("results page")
        
        # 2. Solve and Enter CAPTCHA
        captcha_solution = solve_captcha_manual(results_page)
        
        if not captcha_solution:
            print("CAPTCHA solution failed or was empty. Exiting.")
            return

        results_page.enter_captcha_solution(captcha_solution)
        print(f"CAPTCHA '{captcha_solution}' entered.")
        
        # 3. Submit the Form
        results_page.submit_form()
        
        print("Script finished. Waiting to show result page...")
        time.sleep(10) # Wait for review
        
    except Exception as e:
        print(f"An error occurred during automation: {e}")
    finally:
        if driver:
            driver.quit()
            print("Browser closed.")


if __name__ == "__main__":
    run_automation(FORM_DATA)
