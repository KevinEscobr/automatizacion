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
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_login_y_agregar_medicina(driver):
    last_email_file = os.path.join(os.path.dirname(__file__), "qa_last_email.txt")
    if os.path.exists(last_email_file):
        with open(last_email_file, "r") as f:
            email = f.read().strip()
        print(f"\n[INFO] Email leido desde qa_last_email.txt: {email}")
    else:
        email = os.getenv("QA_EMAIL")
        print(f"\n[INFO] qa_last_email.txt no encontrado, usando QA_EMAIL: {email}")

    password = os.getenv("QA_PASSWORD")

    assert email, "No se encontro email en qa_last_email.txt ni en QA_EMAIL"
    assert password, "La variable de entorno QA_PASSWORD no esta definida"

    # Abrir la pagina
    driver.get("https://despensalo.cl/")
    wait = WebDriverWait(driver, 15)

    # Hacer click en la pestana Iniciar sesion
    btn_tab_login = wait.until(
        EC.element_to_be_clickable((By.ID, "authTabLogin"))
    )
    btn_tab_login.click()

    # Localizar campos del formulario de login
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

    # Enviar formulario de login
    btn_submit.click()

    # Validar mensaje de respuesta del login
    auth_msg = wait.until(
        EC.visibility_of_element_located((By.ID, "authMsg"))
    )
    wait.until(lambda d: len(auth_msg.text.strip()) > 0)
    print(f"\n[LOGIN] Mensaje de autenticacion: {auth_msg.text}")
    assert auth_msg.is_displayed()


    # Navegar a la seccion de medicamentos (data-target="medicineSection")
    btn_medicine_section = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-target="medicineSection"]'))
    )
    btn_medicine_section.click()
    print("\n[NAV] Seccion medicamentos abierta")

    # Esperar que la seccion de medicamentos sea visible
    medicine_section = wait.until(
        EC.visibility_of_element_located((By.ID, "medicineSection"))
    )
    assert medicine_section.is_displayed(), "La seccion medicamentos no esta visible"

    # Hacer click en el boton 'Agregar producto' dentro de la seccion
    btn_add = wait.until(
        EC.element_to_be_clickable((By.ID, "btnAddMedicine"))
    )
    btn_add.click()
    print("\n[ACCION] Click en btnAddMedicine realizado")

    # Esperar que el campo nombre sea visible (confirma que el formulario abrio)
    input_name = wait.until(
        EC.visibility_of_element_located((By.ID, "pName"))
    )
    print("\n[OK] Formulario de agregar producto visible")
    input_name.clear()
    input_name.send_keys("Paracetamol Test")
    print("[FORM] pName ingresado")

    # Marca
    input_brand = driver.find_element(By.ID, "pBrand")
    input_brand.clear()
    input_brand.send_keys("Laboratorio QA")
    print("[FORM] pBrand ingresado")

    # Tamano / cantidad  (valor negativo para verificar validacion)
    input_size = driver.find_element(By.ID, "pSize")
    input_size.clear()
    input_size.send_keys("-5")
    print("[FORM] pSize ingresado con valor negativo (-5) para verificar validacion")

    # Fecha de vencimiento
    input_expiry = driver.find_element(By.ID, "pExpiry")
    input_expiry.clear()
    input_expiry.send_keys("2025-12-31")
    print("[FORM] pExpiry ingresado")

    # Precio unitario
    input_price = driver.find_element(By.ID, "pPrice")
    input_price.clear()
    input_price.send_keys("990")
    print("[FORM] pPrice ingresado")

    # Precio total
    input_price_total = driver.find_element(By.ID, "pPriceTotal")
    input_price_total.clear()
    input_price_total.send_keys("4950")
    print("[FORM] pPriceTotal ingresado")

    time.sleep(3)

    # Guardar el producto
    btn_save = wait.until(
        EC.element_to_be_clickable((By.ID, "btnSaveProduct"))
    )
    btn_save.click()
    print("\n[ACCION] Click en btnSaveProduct realizado")

    # Pausa de visualizacion para ver el resultado
    time.sleep(15)
