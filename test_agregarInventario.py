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

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def _get_last_email() -> str:
    last_file = os.path.join(os.path.dirname(__file__), "qa_last_email.txt")
    if os.path.exists(last_file):
        with open(last_file, "r") as f:
            email = f.read().strip()
            if email:
                return email
    # Fallback: usar QA_EMAIL directo si no hay archivo
    return os.getenv("QA_EMAIL", "")


def _get_next_product_suffix() -> str:
    return uuid.uuid4().hex[:8]

def test_login_y_agregar_inventario(driver):
    # 1. Obtener credenciales y sufijo de producto
    email = _get_last_email()
    password = os.getenv("QA_PASSWORD")
    prod_num = _get_next_product_suffix()
    print(f"\n[INFO] Haciendo login con: {email}")
    print(f"[INFO] Numero de producto esta ejecucion: {prod_num}")

    assert email, "La variable de entorno QA_EMAIL no esta definida"
    assert password, "La variable de entorno QA_PASSWORD no esta definida"

    # 2. Abrir la pagina
    driver.get("https://despensalo.cl/")
    wait = WebDriverWait(driver, 15)

    # ─── BLOQUE LOGIN ────────────────────────────────────────────────────────────

    # 3. Hacer click en la pestana Iniciar sesion
    btn_tab_login = wait.until(
        EC.element_to_be_clickable((By.ID, "authTabLogin"))
    )
    btn_tab_login.click()

    # 4. Localizar campos del formulario de login
    input_email = wait.until(
        EC.visibility_of_element_located((By.ID, "loginEmail"))
    )
    input_pass = driver.find_element(By.ID, "loginPassword")
    btn_submit = driver.find_element(By.ID, "btnLogin")

    # 5. Ingresar credenciales
    input_email.clear()
    input_email.send_keys(email)

    input_pass.clear()
    input_pass.send_keys(password)

    # 6. Enviar formulario de login
    btn_submit.click()

    # 7. Validar mensaje de respuesta del login
    auth_msg = wait.until(
        EC.visibility_of_element_located((By.ID, "authMsg"))
    )
    wait.until(lambda d: len(auth_msg.text.strip()) > 0)
    print(f"\n[LOGIN] Mensaje de autenticacion: {auth_msg.text}")
    assert auth_msg.is_displayed()

    # ─── BLOQUE AGREGAR PRODUCTO AL INVENTARIO ───────────────────────────────────

    # 8. Navegar a la seccion de medicamentos (mismo formulario)
    btn_inventory_section = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-target="inventorySection"]'))
    )
    btn_inventory_section.click()
    print("\n[NAV] Seccion inventario abierta")

    # 9. Esperar que la seccion sea visible
    inventory_section = wait.until(
        EC.visibility_of_element_located((By.ID, "inventorySection"))
    )
    assert inventory_section.is_displayed(), "La seccion de inventario no esta visible"

    # 10. Hacer click en el boton 'Agregar producto'
    btn_add = wait.until(
        EC.element_to_be_clickable((By.ID, "btnAddManual"))
    )
    btn_add.click()
    print("\n[ACCION] Click en btnAddManual realizado")

    # ─── BLOQUE RELLENAR FORMULARIO ──────────────────────────────────────────────

    # 11. Esperar que el formulario abra (campo nombre visible)
    input_name = wait.until(
        EC.visibility_of_element_located((By.ID, "pName"))
    )
    print("\n[OK] Formulario de agregar producto visible")
    input_name.clear()
    input_name.send_keys(f"Producto Inventario Test {prod_num}")
    print(f"[FORM] pName ingresado: Producto Inventario Test {prod_num}")

    # 12. Marca
    input_brand = driver.find_element(By.ID, "pBrand")
    input_brand.clear()
    input_brand.send_keys(f"Marca QA Inventario {prod_num}")
    print(f"[FORM] pBrand ingresado: Marca QA Inventario {prod_num}")

    # 13. Tamaño / cantidad  (valor valido positivo)
    input_size = driver.find_element(By.ID, "pSize")
    input_size.clear()
    input_size.send_keys("-5")
    print("[FORM] pSize ingresado con valor negativo (-5) para verificar validacion de error")

    # 14. Fecha de vencimiento
    input_expiry = driver.find_element(By.ID, "pExpiry")
    input_expiry.clear()
    input_expiry.send_keys("2026-06-30")
    print("[FORM] pExpiry ingresado")

    # 15. Precio unitario
    input_price = driver.find_element(By.ID, "pPrice")
    input_price.clear()
    input_price.send_keys("1500")
    print("[FORM] pPrice ingresado")

    # 16. Precio total
    input_price_total = driver.find_element(By.ID, "pPriceTotal")
    input_price_total.clear()
    input_price_total.send_keys("15000")
    print("[FORM] pPriceTotal ingresado")

    time.sleep(3)

    # 17. Guardar el producto
    btn_save = wait.until(
        EC.element_to_be_clickable((By.ID, "btnSaveProduct"))
    )
    btn_save.click()
    print("\n[ACCION] Click en btnSaveProduct realizado")

    # 18. Pausa de visualizacion para ver el resultado
    time.sleep(8)
