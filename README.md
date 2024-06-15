# Script de Automatización para Consulta de EPS en ADRES

Este script automatiza el proceso de consulta de EPS en el sitio web de ADRES usando Selenium y Anticaptchaofficial.

## Requisitos

- Python 3.x
- `msedgedriver.exe` en el PATH del sistema (para Selenium con Edge)
- Clave de API de Anticaptchaofficial

## Instalación

1. Clona este repositorio o descarga el código.
2. Instala las dependencias usando pip:

   ```bash
   pip install -r requirements.txt
   ```

Asegúrate de tener instalado `msedgedriver.exe` y configurado en el PATH del sistema.

## Configuración

Antes de ejecutar el script, asegúrate de configurar la clave de API de Anticaptchaofficial en el archivo main.py:

```python
# Cambia el valor por la API_KEY de Anticaptchaoficial
ANTI_CAPTCHA_KEY = 'YOUR_ANTICAPTCHA_KEY'
```

## Uso

Ejecuta el script desde la línea de comandos proporcionando el tipo de documento y número de documento como argumentos:

```bash
python main.py CC 1234567890
```

Esto abrirá un navegador automatizado, completará el formulario con los datos proporcionados y guardará la página consultada como PDF y HTML.
