from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from anticaptchaofficial.imagecaptcha import *
import requests
import time
import json

# Cambia el valor por la API_KEY de Anticaptchaoficial
ANTI_CAPTCHA_KEY = '7a7cc7e7d44f7c6139028cbfacc4f900'

def configurar_driver():
    # Configurar el WebDriver de Edge
    edge_options = Options()
    edge_options.add_experimental_option("detach", True)

    # Configuración para guardar como PDF
    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps({
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": ""
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        })
    }
    edge_options.add_experimental_option('prefs', prefs)
    edge_options.add_argument('--kiosk-printing')
    driver = webdriver.Edge(options=edge_options) # Asegúrate de que msedgedriver.exe está en tu PATH
    return driver

def navegar_a_pagina(driver):
    # URL de la pagina a testear
    driver.get("https://www.adres.gov.co/consulte-su-eps")

    # Posicionarse dentro del IFrame donde se encuentra el formulario
    driver.switch_to.frame(0)

def llenar_formulario(driver, tipo_documento, numero_documento):
    # Seleccionar el tipo de documento
    select_tipo_documento = Select(driver.find_element(By.ID, "tipoDoc"))
    select_tipo_documento.select_by_value(tipo_documento)

    # Introducir el número de documento
    input_numero_documento = driver.find_element(By.ID, "txtNumDoc")
    input_numero_documento.send_keys(numero_documento)

def obtener_captcha_image_url(driver):
    # Obtener la URL de la imagen del CAPTCHA
    captcha_image_element = driver.find_element(By.ID, 'Capcha_CaptchaImageUP')
    return captcha_image_element.get_attribute('src')

def descargar_captcha(captcha_image_url):
    # Descargar la imagen del CAPTCHA sin verificar el certificado SSL
    captcha_image_response = requests.get(captcha_image_url, verify=False)
    with open("captcha.png", "wb") as file:
        file.write(captcha_image_response.content)

def resolver_captcha():
    # Resolver imageCaptcha usando Anticaptchaoficial
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(ANTI_CAPTCHA_KEY)
    captcha_text = solver.solve_and_return_solution("captcha.png")
    if captcha_text == 0:
        raise Exception(f"Error resolving captcha: {solver.error_code}")
    return captcha_text

def introducir_captcha(driver, captcha_text):
    # Introducir el valor obtenido del captcha
    captcha_input = driver.find_element(By.ID, "Capcha_CaptchaTextBox")
    captcha_input.send_keys(captcha_text)

def hacer_click_en_consultar(driver):
    # Hacer clic en el botón de consultar
    boton_consultar = driver.find_element(By.ID, "btnConsultar")
    boton_consultar.click()

def cambiar_a_nueva_ventana(driver):
    # Esperar a que la nueva ventana se abra y cambiar el foco a la nueva ventana
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[1])

def guardar_pagina_como_pdf(driver):
    # Guardar la página como PDF
    driver.execute_script('window.print();')

def guardar_pagina_como_html(driver):
    # Guardar la página como HTML
    with open("consulta.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

def main():
    driver = configurar_driver()
    try:
        navegar_a_pagina(driver)
        llenar_formulario(driver, 'CC', '1006417460')
        captcha_image_url = obtener_captcha_image_url(driver)
        descargar_captcha(captcha_image_url)
        captcha_text = resolver_captcha()
        introducir_captcha(driver, captcha_text)
        hacer_click_en_consultar(driver)
        cambiar_a_nueva_ventana(driver)
        time.sleep(3)  # Esperar a que la nueva página cargue completamente
        guardar_pagina_como_pdf(driver)
        guardar_pagina_como_html(driver)
    finally:
        time.sleep(3)  # Esperar antes de cerrar el navegador para asegurar que se guarde correctamente
        driver.quit()

if __name__ == "__main__":
    main()
