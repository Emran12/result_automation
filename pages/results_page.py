import time # Import time for simple waits (should be replaced by WebDriverWait for production)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class ResultsPage:
    """
    Page Object Model for the Result Form page.
    Contains all locators and methods for interacting with the form elements.
    """
    
    def __init__(self, driver):
        """Initializes the page object with the WebDriver instance."""
        self.driver = driver
        
        # --- Locators (Defined using By tuples) ---
        # STANDARD DROPDOWN LOCATORS (Assumed to be <select> elements)
        self.EXAM_DROPDOWN = (By.ID, "exam")        
        self.YEAR_DROPDOWN = (By.ID, "year")        
        self.RESULT_TYPE_DROPDOWN = (By.ID, "result_type") 

        # CUSTOM DROPDOWN LOCATORS (For the complex Board field)
        # 1. Locator for the visible element (the button/div that opens the list)
        self.BOARD_OPEN_BUTTON = (By.ID, "board") 
        
        
        # INPUT AND BUTTON LOCATORS
        self.ROLL_INPUT = (By.ID, "roll")      
        self.REG_INPUT = (By.XPATH, '//div[@id="row_reg"]//input[@id="reg"]')        
        self.CAPTCHA_IMAGE = (By.ID, "captcha_img") 
        self.CAPTCHA_INPUT = (By.ID, "captcha") 
        self.SUBMIT_BUTTON = (By.ID, "submit") 

    # --- Interaction Methods ---
    def select_standard_dropdown(self, button, data, key):
        """
        Handles selection for a custom-styled dropdown menu.
        Clicks the visible dropdown trigger, then selects the desired option by text.
        """
        try:
            print(f"Selecting {key}: {data[key]} using custom click sequence.")

            # Step 1: Click dropdown to open the visible list
            open_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(button)
            )
            open_button.click()
            time.sleep(0.5)

            # Step 2: Find the visible option (adjust locator depending on HTML structure)
            option_xpath = f'//select[@id="{key}"]/option[@value="{data[key]}"]'
            print("option_xpath:", option_xpath)

            option_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, option_xpath))
            )

            # Step 3: Scroll to and click the visible option
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                option_element
            )
            time.sleep(0.3)
            option_element.click()

            # Step 4: Click outside to close dropdown
            self.driver.find_element(By.TAG_NAME, "body").click()
            print(f"✅ Successfully selected custom {key}: {data[key]}.")

        except Exception as e:
            print(f"❌ Error selecting custom board dropdown value: {e}")



    def fill_input_field(self, locator, text):
        """Generic method to enter text into an input field."""
        self.driver.find_element(*locator).send_keys(text)
        print(f"Entered text in {locator[1]}: {text}")
        
    def submit_form(self):
        """Clicks the main submit button."""
        self.driver.find_element(*self.SUBMIT_BUTTON).click()
        print("Form submitted.")

    # --- Specific Form Interaction Wrappers ---
    
    def fill_form_data(self, data):
        """Fills all fields using the data dictionary."""
        
        # Select Dropdowns
        # Board, EXAM, YEAR, RESULT_TYPE use the standard <select> method
        self.select_standard_dropdown(self.BOARD_OPEN_BUTTON, data, "board") 
        self.select_standard_dropdown(self.EXAM_DROPDOWN, data, "exam")
        self.select_standard_dropdown(self.YEAR_DROPDOWN, data, "year")
        self.select_standard_dropdown(self.RESULT_TYPE_DROPDOWN, data, "result_type")
       
        # Fill Inputs
        self.fill_input_field(self.ROLL_INPUT, data["roll_number"])
        self.fill_input_field(self.REG_INPUT, data["reg_number"])

    def enter_captcha_solution(self, solution):
        """Enters the provided CAPTCHA solution."""
        self.fill_input_field(self.CAPTCHA_INPUT, solution)
        
    def save_captcha_image(self):
        """Saves the CAPTCHA image for manual or service solving."""
        try:
            captcha_element = self.driver.find_element(*self.CAPTCHA_IMAGE)
            captcha_element.screenshot("current_captcha.png")
            return True
        except Exception as e:
            print(f"Could not save CAPTCHA image: {e}")
            return False
