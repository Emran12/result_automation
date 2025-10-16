import os
from selenium import webdriver
# --- NEW IMPORTS ---
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager 

def get_chrome_driver(driver_path=None, chrome_binary_path=None, is_headless=False): # <-- NEW: is_headless argument
    """
    Initializes and returns a configured Chrome WebDriver instance.

    This version uses webdriver_manager for automatic driver management (best for Linux).

    Args:
        driver_path (str, optional): Now unused, retained for signature compatibility.
        chrome_binary_path (str, optional): Explicit path to the Chrome browser executable (binary).
        is_headless (bool, optional): If True, runs Chrome in headless mode (no visible GUI). Defaults to False.

    Returns:
        webdriver.Chrome: A configured WebDriver instance, or None if initialization fails.
    """
    try:
        options = Options()
        
        # 1. Handle Chrome Binary Location
        if chrome_binary_path and os.path.exists(chrome_binary_path):
            options.binary_location = chrome_binary_path
            print(f"Using Chrome binary at: {chrome_binary_path}")
        
        # 2. Add common arguments for stability, especially on Linux/CI environments
        options.add_argument("--no-sandbox")            # Required in some Linux environments
        options.add_argument("--disable-dev-shm-usage")  # Recommended for stability
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--window-size=1920,1080")  # Set a defined window size

        # 3. Handle Headless Mode
        if is_headless:
            options.add_argument("--headless=new")      # Use new headless mode
            print("Running in HEADLESS mode.")
        else:
            options.add_argument("--start-maximized")   # Maximize window if running visible
        
        # 4. Use webdriver-manager to get the service path
        service = ChromeService(ChromeDriverManager().install())
        
        # 5. Initialize the driver
        driver = webdriver.Chrome(service=service, options=options) 

        print("WebDriver initialized and browser opened successfully.")
        
        # NOTE: driver.maximize_window() is redundant if using --start-maximized option, 
        # but we include it here for compatibility if the option is overridden.
        if not is_headless:
            driver.maximize_window()

        return driver
    
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        print("Ensure the 'webdriver-manager' package is installed and Google Chrome/Chromium is installed on your system.")
        return None
