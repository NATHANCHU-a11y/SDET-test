from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Lock, Thread
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def initialize_webdriver():
    """
    Initializes and returns a Selenium WebDriver with Chrome.
    """
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get('http://sdetchallenge.fetch.com/')
    return driver


def reset_button(driver):
    """
    Clicks the reset button on the page to clear any previous inputs.
    """
    try:
        reset_buttons = driver.find_elements(By.ID, "reset")
        reset_buttons[1].click()
    except IndexError:
        logging.error("Reset button not found in the expected position.")


def weigh_bars(driver, left_bars, right_bars):
    """
    Inputs numbers into the left and right scales and performs the weighing.
    Parameters:
        driver (WebDriver): The Selenium WebDriver.
        left_bars (list): List of integers representing bar indices on the left scale.
        right_bars (list): List of integers representing bar indices on the right scale.
    Returns:
        str: The result of the weighing.
    """
    try:
        # Enter bar numbers into the left and right bowls
        for i, bar in enumerate(left_bars):
            driver.find_element(By.ID, f'left_{i}').send_keys(str(bar))

        for i, bar in enumerate(right_bars):
            driver.find_element(By.ID, f'right_{i}').send_keys(str(bar))

        # Click the weigh button
        weigh_button = driver.find_element(By.ID, "weigh")
        weigh_button.click()

        # Wait for and get the result of the weighing
        WebDriverWait(driver, 20).until(
            lambda wait: driver.find_element(By.CLASS_NAME, "result").find_element(By.ID, "reset").text != "?")
        results = driver.find_element(By.CLASS_NAME, "result").find_element(By.ID, "reset").text
        return results
    except Exception as e:
        logging.error("Error during weighing: %s", e)
        return None


def find_fake_bar(driver):
    """
    Determines which bar is fake by comparing weights and handles any alerts.
    """
    try:
        # Weigh first three groups
        result = weigh_bars(driver, [0, 1, 2], [3, 4, 5])
        if result == "<":
            suspicious_bars = [0, 1, 2]
        elif result == ">":
            suspicious_bars = [3, 4, 5]
        else:
            suspicious_bars = [6, 7, 8]

        # Narrow down to one bar
        reset_button(driver)
        result = weigh_bars(driver, [suspicious_bars[0]], [suspicious_bars[1]])
        if result == "<":
            fake_bar = suspicious_bars[0]
        elif result == ">":
            fake_bar = suspicious_bars[1]
        else:
            fake_bar = suspicious_bars[2]

        fake_button = driver.find_element(By.ID, f'coin_{fake_bar}')
        fake_button.click()

        # Handle the alert message if any appears
        alert = WebDriverWait(driver, 20).until(EC.alert_is_present())
        message = alert.text
        alert.accept()
        return message
    finally:
        driver.quit()


def thread_function(success_count, lock):
    """
    Function to be executed by each thread. Tests the find_fake_bar function.
    Updates a shared counter if the test was successful.
    """
    try:
        driver = initialize_webdriver()
        message = find_fake_bar(driver)
        if message == "Yay! You find it!":
            with lock:
                success_count[0] += 1
    except Exception as e:
        logging.error("Thread encountered an error: %s", e)


num_threads = 5
success_count = [0]
lock = Lock()
threads = []

for _ in range(num_threads):
    t = Thread(target=thread_function, args=(success_count, lock))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

if success_count[0] == num_threads:
    logging.info("Test success: All threads reported success!")
else:
    logging.error("Test failed: Not all threads were successful.")
