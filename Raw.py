from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from anticaptchaofficial.imagecaptcha import *
import requests
import time
import json

ANTI_CAPTCHA_KEY = '7a7cc7e7d44f7c6139028cbfacc4f900'

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

driver = webdriver.Edge(options=edge_options)  # Asegúrate de que msedgedriver.exe está en tu PATH

driver.get("https://www.adres.gov.co/consulte-su-eps")

# Posicionarse dentro del IFrame donde se encuentra el formulario
driver.switch_to.frame(0)

# Seleccionar el tipo de documento
select_tipo_documento = Select(driver.find_element(By.ID, "tipoDoc"))
select_tipo_documento.select_by_value('CC')  # Ejemplo: CC para cédula de ciudadanía

# Introducir el número de documento
input_numero_documento = driver.find_element(By.ID, "txtNumDoc")
input_numero_documento.send_keys('1006417460')

# Resolver el CAPTCHA

# Obtener la URL de la imagen del CAPTCHA
captcha_image_element = driver.find_element(By.ID, 'Capcha_CaptchaImageUP')
captcha_image_url = captcha_image_element.get_attribute('src')

# Descargar la imagen del CAPTCHA sin verificar el certificado SSL
captcha_image_response = requests.get(captcha_image_url, verify=False)
with open("captcha.png", "wb") as file:
    file.write(captcha_image_response.content)

solver = imagecaptcha()
solver.set_verbose(1)
solver.set_key(ANTI_CAPTCHA_KEY)

captcha_text = solver.solve_and_return_solution("captcha.png")
if captcha_text != 0:
    print("captcha text " + captcha_text)
else:
    print("task finished with error " + solver.error_code)

# Introducir el valor obtenido del captcha
captcha_input = driver.find_element(By.ID, "Capcha_CaptchaTextBox")
captcha_input.send_keys(captcha_text)

# Hacer clic en el botón de consultar
boton_consultar = driver.find_element(By.ID, "btnConsultar")
boton_consultar.click()

# Esperar a que la nueva ventana se abra y cambiar el foco a la nueva ventana
time.sleep(5)  # Ajusta el tiempo según sea necesario
driver.switch_to.window(driver.window_handles[1])

# Esperar a que la nueva página cargue completamente
time.sleep(5)  # Ajusta el tiempo según sea necesario

# Guardar la página como PDF
driver.execute_script('window.print();')

# Guardar la página como HTML
with open("pagina.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

# Cerrar el navegador después de un breve retraso para asegurar que el PDF se guarde correctamente
time.sleep(5)
driver.quit()
