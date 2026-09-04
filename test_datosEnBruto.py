import os
import time
import uuid
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # Abre la consola de desarrollador (DevTools) automáticamente
    options.add_argument("--auto-open-devtools-for-tabs")
    
    driver = webdriver.Chrome(options=options)

    # Activar la pestaña Network en DevTools via CDP
    driver.execute_cdp_cmd("Network.enable", {})

    yield driver
    driver.quit()

def _get_next_email(base_email: str) -> str:
    uid = uuid.uuid4().hex[:8]
    if "@" in base_email:
        local, domain = base_email.split("@", 1)
        email = f"{local}{uid}@{domain}"
    else:
        email = f"{base_email}{uid}"
    _save_last_email(email)
    return email


def _save_last_email(email: str) -> None:
    last_file = os.path.join(os.path.dirname(__file__), "qa_last_email.txt")
    with open(last_file, "w") as f:
        f.write(email)


def test_registro_usuario(driver):
    # 1. Obtener correo y contraseña (de variables de entorno o predeterminados)
    base_email = os.getenv("QA_EMAIL", "")
    email = _get_next_email(base_email)
    print(f"\n[INFO] Email usado en esta ejecución: {email}")
    password = os.getenv("QA_PASSWORD")

    # 2. Abrir la página
    driver.get("https://despensalo.cl/")
    wait = WebDriverWait(driver, 15)

    # 3. Dar click en la pestaña 'Crear cuenta' (Registro)
    btn_tab_register = wait.until(
        EC.element_to_be_clickable((By.ID, "authTabRegister"))
    )
    btn_tab_register.click()

    # 4. Localizar campos del formulario de registro
    input_email = wait.until(
        EC.visibility_of_element_located((By.ID, "registerEmail"))
    )
    input_pass = driver.find_element(By.ID, "registerPassword")
    input_pass2 = driver.find_element(By.ID, "registerPassword2")
    btn_submit = driver.find_element(By.ID, "btnRegister")

    # 5. Ingresar credenciales
    input_email.clear()
    input_email.send_keys(email)

    input_pass.clear()
    input_pass.send_keys(password)

    input_pass2.clear()
    input_pass2.send_keys(password)

    # 6. Presionar botón de registro
    btn_submit.click()

    # 7. Validar mensaje de respuesta en la interfaz
    auth_msg = wait.until(
        EC.visibility_of_element_located((By.ID, "authMsg"))
    )
    wait.until(lambda d: len(auth_msg.text.strip()) > 0)
    print(f"\n[UI] Mensaje mostrado en pantalla: {auth_msg.text}")
    assert auth_msg.is_displayed()

    # 8. Pausa de visualización
    time.sleep(30)
