import os
import pytest
from selenium import webdriver

BASE_URL = "http://127.0.0.1:8000"
SHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "images")


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    d = webdriver.Chrome(options=options)
    d.maximize_window()
    d.implicitly_wait(5)
    yield d
    os.makedirs(SHOT_DIR, exist_ok=True)
    d.save_screenshot(os.path.join(SHOT_DIR, f"selenium-{request.node.name}.png"))
    d.quit()


@pytest.fixture
def base_url():
    return BASE_URL