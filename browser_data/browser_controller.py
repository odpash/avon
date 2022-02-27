import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser_data import parse_statistic
from browser_data import excel


driver_path = "/Users/olegpash/PycharmProjects/avon/browser_data/chromedriver"

login_link = "https://my.avon.ru/menedzher/predstavitel/"
catalog_url = "https://www.avon.ru/REPSuite/orderEntry.page"
order_url = "https://www.avon.ru/REPSuite/orderSummary.page"


def login_avon(driver, login, password):
    driver.get(catalog_url)
    driver.find_element(By.NAME, "userIdDisplay").send_keys(login)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.ID, "submitBtn").click()


def clear_order(driver):
    driver.find_element(By.ID, "bread_crumb_completeorder").click()
    time.sleep(3)
    driver.refresh()
    time.sleep(2)
    y = 2500
    driver.execute_script(f"window.scrollTo(0, {y})")
    time.sleep(2)
    driver.find_elements(By.CLASS_NAME, "cb-uc")[4].click()  # delete checkbox
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'button[class="btn pao__avon-btn pao__avon-btn--outline text-capitalize w-100 float-right waves-effect waves-light"]').click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    time.sleep(2)


def form_order(driver, items):
    index = -1
    # добавление заказов
    y = 600
    for i in items:
        y = y + 50
        index = index + 1
        time.sleep(1)
        driver.find_element(By.ID, f"newItems[{index}].linenumber").send_keys(i[0])
        element = driver.find_element(By.ID, f"newItems[{index}].quantity")
        element.clear()
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        time.sleep(1)
        element.send_keys(i[1])
        time.sleep(2)
        driver.find_element(By.ID, f"suggestionstab_{index + 1}").click()
        driver.execute_script(f"window.scrollTo(0, {y})")
    driver.find_element(By.CSS_SELECTOR,
                        'div[class="text-center Order-Entry_header_normal cursor__pointer breadcrumb-spacing"]').click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,
                        'div[class="text-center Order-Entry_header_normal cursor__pointer breadcrumb-spacing"]').click()

    driver.find_element(By.ID, "bread_crumb_completeorder").click()
    time.sleep(2)


def delete_other_products(driver, items):
    y = 2500
    driver.execute_script(f"window.scrollTo(0, {y})")
    time.sleep(2)
    driver.find_elements(By.CLASS_NAME, "cb-uc")[4].click()  # delete checkbox
    time.sleep(1)
    for i in range(len(items)):
        driver.find_elements(By.CLASS_NAME, "cb-c")[5 + i].click()
        time.sleep(1)
    driver.find_element(By.NAME, "servedCustomerCount").send_keys("1")
    driver.find_element(By.CSS_SELECTOR, 'button[class="btn pao__avon-btn text-capitalize w-40 waves-effect waves-light"]').click()
    time.sleep(3)


def main(login, password, items, is_to_order):
    driver = webdriver.Chrome(driver_path)
    login_avon(driver, login, password)
    # закрытие рекламы
    driver.find_element(By.CSS_SELECTOR, 'a[data-link="PlaceAnOrder_skip_x"]').click()
    driver.find_element(By.CSS_SELECTOR, 'button[data-button="PAO_Step0_Contine_Order"]').click()
    time.sleep(2)
    # закрытие рекламы
    try:
        clear_order(driver)  # если корзина не пуста
    except:
        time.sleep(1)
    form_order(driver, items)
    delete_other_products(driver, items)
    answer = driver.page_source
    if is_to_order:
        driver.execute_script(f"window.scrollTo(0, {3000})")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'div[class="cb-uc"]').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'button[class="btn pao__avon-btn pull-right text-capitalize w-50 float-right waves-effect waves-light"]').click()
        time.sleep(3)
    driver.close()
    return answer


def order(fi, login, password, items, order_id, is_to_order):
    html = main(login, password, items, is_to_order)
    statistic, finaly_info = parse_statistic.parse_statistic(html, fi, login, password)
    report_addr = excel.write_report(statistic, finaly_info, fi, login, password, order_id)
    return report_addr


#order("Пащенко Олег", "104812115", "Dubliners63", [["11671", "1"]], '4', False)
