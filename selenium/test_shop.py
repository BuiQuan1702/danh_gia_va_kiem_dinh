import os
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

EMAIL = os.environ.get("SHOP_EMAIL", "")
PASSWORD = os.environ.get("SHOP_PASSWORD", "")
PRODUCT_SLUG = "vay-len-basic"
PRODUCT_NAME = "Váy len basic"


def open_login(driver, base_url):
    driver.get(f"{base_url}/login")


def submit_login(driver):
    driver.find_element(By.CSS_SELECTOR, "#login-form button[type='submit']").click()


def login(driver, base_url):
    open_login(driver, base_url)
    driver.find_element(By.ID, "email").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    submit_login(driver)
    WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)


def add_to_cart(driver, base_url):
    driver.get(f"{base_url}/products/{PRODUCT_SLUG}")
    old_form = driver.find_element(By.ID, "product-add-form")
    driver.find_element(By.ID, "product-add-button").click()
    try:
        WebDriverWait(driver, 10).until(EC.staleness_of(old_form))
    except TimeoutException:
        pass


def cart_quantity_value(driver, base_url):
    driver.get(f"{base_url}/cart")
    box = driver.find_element(By.CSS_SELECTOR, "input[name='quantity'][id^='cart-quantity-']")
    return box.get_attribute("value")


def test_tc01_login_thanh_cong(driver, base_url):
    open_login(driver, base_url)
    driver.find_element(By.ID, "email").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    submit_login(driver)
    WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)
    assert "/login" not in driver.current_url


def test_tc02_login_sai_mat_khau(driver, base_url):
    open_login(driver, base_url)
    old_form = driver.find_element(By.ID, "login-form")
    driver.find_element(By.ID, "email").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys("sai_mat_khau_123")
    submit_login(driver)
    WebDriverWait(driver, 10).until(EC.staleness_of(old_form))
    assert "/login" in driver.current_url
    assert driver.find_element(By.ID, "login-form").is_displayed()


def test_tc03_login_bo_trong_email(driver, base_url):
    open_login(driver, base_url)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    submit_login(driver)
    email = driver.find_element(By.ID, "email")
    assert driver.execute_script("return arguments[0].validity.valueMissing", email)
    assert "/login" in driver.current_url


def test_tc04_tim_kiem_san_pham(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.CSS_SELECTOR, "#shop-search-details summary").click()
    box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#shop-search-details input[name='q']")
        )
    )
    box.send_keys("len", Keys.ENTER)
    WebDriverWait(driver, 10).until(lambda d: "q=len" in d.current_url)
    assert "/products" in driver.current_url
    assert PRODUCT_NAME in driver.page_source


def test_tc05_xem_chi_tiet_san_pham(driver, base_url):
    driver.get(f"{base_url}/products/{PRODUCT_SLUG}")
    assert PRODUCT_NAME in driver.title
    assert "289.000" in driver.page_source


def test_tc06_them_san_pham_vao_gio(driver, base_url):
    login(driver, base_url)
    add_to_cart(driver, base_url)
    driver.get(f"{base_url}/cart")
    assert PRODUCT_NAME in driver.page_source
    badge = driver.find_element(By.CSS_SELECTOR, ".nd-cart-badge").text
    assert badge.isdigit() and int(badge) >= 1


def test_tc07_cap_nhat_so_luong_trong_gio(driver, base_url):
    login(driver, base_url)
    add_to_cart(driver, base_url)
    driver.get(f"{base_url}/cart")
    box = driver.find_element(By.CSS_SELECTOR, "input[name='quantity'][id^='cart-quantity-']")
    box.send_keys(Keys.CONTROL, "a")
    box.send_keys("3", Keys.ENTER)
    time.sleep(2)
    value = None
    for _ in range(8):
        value = cart_quantity_value(driver, base_url)
        if value == "3":
            break
        time.sleep(1)
    assert value == "3"


def test_tc08_dang_xuat(driver, base_url):
    login(driver, base_url)
    driver.get(base_url)
    driver.find_element(By.CSS_SELECTOR, "#shop-account-details summary").click()
    logout_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#shop-account-details form[action$='/logout'] button")
        )
    )
    logout_btn.click()
    WebDriverWait(driver, 10).until(EC.staleness_of(logout_btn))
    assert len(driver.find_elements(By.ID, "shop-account-details")) == 0
    assert len(driver.find_elements(By.CSS_SELECTOR, "a[href$='/login']")) >= 1