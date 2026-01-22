
import requests
import json
import time

url = "http://127.0.0.1:8000/api/generar"

# Guion SECUENCIAL diseñado para activar TODOS los templates de uno en uno
# orden: Intro -> LowerThird -> Bar Chart -> Pie Chart -> List -> Quote
sequential_script = """
Demostración Completa.
Bienvenidos a la prueba secuencial.

Mi nombre es Ana y esto es el Lower Third.
Vamos a probar cada elemento visual.

Primero, un gráfico de barras usual para analizar los datos.
Los datos muestran un crecimiento del 85% en ventas durante este año fiscal.
El gráfico de barras debe aparecer aquí claramente visible en pantalla.

Ahora pasemos a la distribución de mercado global y local.
Esta tarta circular muestra cómo nos dividimos en diferentes sectores de la industria tecnológica.
El gráfico de tarta (Pie Chart) debe aparecer ahora mostrando los porcentajes correctos.

Continuamos con una lista de pasos esenciales para el éxito del proyecto.
1. Planificar con detalle. 2. Ejecutar con precisión. 3. Verificar los resultados obtenidos.
Estos puntos son clave para asegurar que todo salga según lo previsto en el plan.

Finalmente, una gran frase inspiradora.
Como dijo Confucio:
El hombre que mueve una montaña empieza apartando pequeñas piedras.

Gracias por su atención.
"""

payload = {
    "script": sequential_script
}

try:
    print("🚀 Enviando guion SECUENCIAL (Intro -> L3 -> KPI -> Pie -> List -> Quote)...")
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Éxito! Video Generado: {data.get('url')}")
    else:
        print(f"❌ Error: {response.text}")
        with open("last_error.txt", "w", encoding="utf-8") as f:
            f.write(response.text)

except Exception as e:
    print(f"❌ Excepción: {e}")
