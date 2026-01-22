
import requests
import json
import time

url = "http://127.0.0.1:8000/api/generar"

# Script with keywords to trigger CHART detection
script_text = """
Introducción a los Datos.
Hola, hoy vamos a hablar de estadísticas importantes.

Aquí tenemos un gráfico con los datos de crecimiento económico.
Es impresionante ver cómo suben los porcentajes cada año.

Fin de la presentación.
"""

payload = {
    "script": script_text
}

try:
    print("🚀 Sending request to generate video with CHARTS (Circular PIP)...")
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! URL: {data.get('url')}")
    else:
        print(f"❌ Failed. See last_error.txt")
        with open("last_error.txt", "w", encoding="utf-8") as f:
            f.write(response.text)

except Exception as e:
    print(f"❌ Exception: {e}")
