import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main(login, password):
    driver_path = "/Users/olegpash/PycharmProjects/avon/browser_data/chromedriver"
    catalog_url = "https://www.avon.ru/REPSuite/orderEntry.page"
    driver = webdriver.Chrome(driver_path)
    driver.get(catalog_url)
    driver.find_element(By.NAME, "userIdDisplay").send_keys(login)
    driver.find_element(By.NAME, "password").send_keys(password)

    driver.find_element(By.ID, "submitBtn").click()
    time.sleep(2)
    d = driver.page_source
    driver.close()
    if "Вы ввели неверный компьютерный номер или пароль. Используйте заглавные буквы латинского алфавита в поле «Компьютерный номер»" in d:
        return False
    else:
        return True
