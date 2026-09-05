import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--window-size=1366,768")
    driver = webdriver.Chrome(options=options)

    yield driver
    driver.quit()


def _read_last_email() -> str:
    """Lee el email generado por test_register.py desde qa_last_email.txt."""
    last_file = os.path.join(os.path.dirname(__file__), "qa_last_email.txt")
    if os.path.exists(last_file):
        with open(last_file, "r") as f:
            return f.read().strip()
    return os.getenv("QA_EMAIL", "")


def test_login_usuario(driver):
    # Usar el email dinámico guardado por test_register.py (fallback a QA_EMAIL)
    email = _read_last_email()
    password = os.getenv("QA_PASSWORD", "")
    print(f"\n[INFO] Email usado en esta ejecución: {email}")
    print(f"[INFO] Resolución: 1366x768")

    # Abrir la página
    driver.get("https://despensalo.cl/")
    wait = WebDriverWait(driver, 15)

    # Localizar campos del formulario de login (pestaña de inicio de sesión activa por defecto)
    input_email = wait.until(
        EC.visibility_of_element_located((By.ID, "loginEmail"))
    )
    input_pass = driver.find_element(By.ID, "loginPassword")
    btn_submit = driver.find_element(By.ID, "btnLogin")

    # Ingresar credenciales
    input_email.clear()
    input_email.send_keys(email)

    input_pass.clear()
    input_pass.send_keys(password)

    # Presionar botón de inicio de sesión
    btn_submit.click()

    # Validar mensaje de respuesta en la interfaz
    auth_msg = wait.until(
        EC.visibility_of_element_located((By.ID, "authMsg"))
    )
    wait.until(lambda d: len(auth_msg.text.strip()) > 0)
    print(f"\n[UI] Mensaje mostrado en pantalla: {auth_msg.text}")
    assert auth_msg.is_displayed()

    # Pausa de visualización
    time.sleep(2)
