from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def initialize_webdriver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get('http://sdetchallenge.fetch.com/')
    return driver


def reset_button(driver):
    # Clear previous inputs by clicking the 'Reset' button
    reset_buttons = driver.find_elements(By.ID, "reset")
    reset_buttons[1].click()


def weigh_bars(driver, left_bars, right_bars):
    print("Left List: " + str(left_bars))
    print("Right List: " + str(right_bars))

    # Enter bar numbers into the left and right bowls
    for i, bar in enumerate(left_bars):
        driver.find_element(By.ID, f'left_{i}').send_keys(str(bar))

    for i, bar in enumerate(right_bars):
        driver.find_element(By.ID, f'right_{i}').send_keys(str(bar))

    # Click the weigh button, assuming it has an ID 'weigh'
    weigh_button = driver.find_element(By.ID, "weigh")
    weigh_button.click()

    # Wait for and get the result of the weighing
    WebDriverWait(driver, 20).until(
        lambda wait: driver.find_element(By.CLASS_NAME, "result").find_element(By.ID, "reset").text != "?")
    results = driver.find_element(By.CLASS_NAME, "result").find_element(By.ID, "reset").text
    print(results)
    return results


def find_fake_bar(driver):
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

    print(f"fake bar is {fake_bar}")
    fake_button = driver.find_element(By.ID, f'coin_{fake_bar}')
    fake_button.click()

    # Handle the alert message if any appears
    try:
        alert = WebDriverWait(driver, 20).until(EC.alert_is_present())
        message = alert.text
        alert.accept()
    except TimeoutException:
        message = "No alert present or alert dismissed"

    return message


driver = initialize_webdriver()
try:
    success = find_fake_bar(driver)
finally:
    driver.quit()
