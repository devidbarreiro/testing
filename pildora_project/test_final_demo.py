
import requests
import json

url = "http://127.0.0.1:8000/api/generar"

# Guion Completo según petición:
# 1. Intro Silenciosa (0-4s de silencio)
# 2. Lower Third (Nombre y Tema)
# 3. Gráficos opacos (PIP)
# 4. Fondo continuo

script_text = """
El Futuro de la IA 2026.
Bienvenidos a este análisis profundo sobre tecnología.

Me llamo Ana y hoy vamos a ver cómo la inteligencia artificial ha cambiado nuestras vidas. Desde la medicina hasta la educación, el impacto es innegable.

Datos de adopción global.
Analizando las estadísticas, vemos que el uso de IA ha crecido un 300% en el último año. El gráfico muestra claramente esta curva exponencial en diferentes sectores.

Como dijo Alan Turing:
Solo podemos ver poco del futuro, pero lo suficiente para darnos cuenta de que hay mucho que hacer.

En resumen, estamos ante una revolución.
"""

payload = {
    "script": script_text
}

try:
    print("🚀 Enviando guion COMPLETO (Intro, Silent, Lower3rd, Chart, Quote)...")
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Éxito Final! Video: {data.get('url')}")
    else:
        print(f"❌ Error: {response.text}")
        with open("last_error.txt", "w", encoding="utf-8") as f:
            f.write(response.text)

except Exception as e:
    print(f"❌ Excepción: {e}")
