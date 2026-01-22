import requests
import time
import os
from django.conf import settings

class HeyGenService:
    BASE_URL = "https://api.heygen.com"
    
    def __init__(self):
        self.api_key = os.getenv("HEYGEN_API_KEY")
        if not self.api_key:
            raise ValueError("HEYGEN_API_KEY no configurada. Por favor revisa tu archivo .env")
            
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def check_credits(self):
        """Verifica si hay créditos disponibles (opcional, para debug)"""
        try:
            # Endpoint ficticio de status o user info, adaptarlo según API real
            # HeyGen no tiene un endpoint simple de 'check credits' público estándar
            # asi que probamos listando videos para ver si la key funciona
            res = requests.get(f"{self.BASE_URL}/v1/video.list", headers=self.headers)
            return res.status_code == 200
        except:
            return False

    def get_avatars(self):
        """Obtiene lista de avatares disponibles"""
        try:
            res = requests.get(f"{self.BASE_URL}/v2/avatars", headers=self.headers)
            if res.status_code == 200:
                return res.json().get("data", {}).get("avatars", [])
            return []
        except Exception as e:
            print(f"Error listing avatars: {e}")
            return []

    def get_voices(self):
        """Obtiene lista de voces disponibles"""
        try:
            res = requests.get(f"{self.BASE_URL}/v2/voices", headers=self.headers)
            if res.status_code == 200:
                return res.json().get("data", {}).get("voices", [])
            return []
        except Exception as e:
            print(f"Error listing voices: {e}")
            return []

    def generate_video(self, text, avatar_id="Angela_inTshirt_20220820", voice_id="131a4362438841a182903c5d6487e41d"):
        """Genera un video hablando el texto dado"""
        
        # 1. Crear el trabajo (Job)
        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": avatar_id,
                        "avatar_style": "normal"
                    },
                    "voice": {
                        "type": "text",
                        "input_text": text,
                        "voice_id": voice_id
                    },
                    "background": {
                        "type": "color",
                        "value": "#1a1a1a"
                    }
                }
            ],
            "dimension": {
                "width": 1280,
                "height": 720
            }
        }
        
        print(f"🚀 Enviando a HeyGen: {text[:30]}... (Avatar: {avatar_id}, Voice: {voice_id})")
        response = requests.post(
            f"{self.BASE_URL}/v2/video/generate",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code != 200:
            error_msg = response.text
            
            # Fallback de Avatar
            if "avatar_not_found" in error_msg:
                print(f"⚠️ Avatar {avatar_id} no encontrado. Reintentando con fallback...")
                avatars = self.get_avatars()
                if avatars:
                    first_id = avatars[0].get('avatar_id')
                    print(f"🔄 Usando avatar: {first_id}")
                    return self.generate_video(text, avatar_id=first_id, voice_id=voice_id)

            # Fallback de Voz
            if "Voice not found" in error_msg or "voice_not_found" in error_msg: 
                print(f"⚠️ Voz {voice_id} no encontrada. Reintentando con fallback...")
                voices = self.get_voices()
                if voices:
                    first_voice = voices[0].get('voice_id')
                    print(f"🔄 Usando voz: {first_voice} ({voices[0].get('name')})")
                    return self.generate_video(text, avatar_id=avatar_id, voice_id=first_voice)

            raise Exception(f"Error HeyGen ({response.status_code}): {response.text}")
            
        data = response.json()
        video_id = data["data"]["video_id"]
        print(f"✅ Trabajo creado. ID: {video_id}")
        
        return video_id

    def wait_for_completion(self, video_id, interval=5, timeout=300):
        """Espera a que el video termine de renderizarse (Polling)"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            response = requests.get(
                f"{self.BASE_URL}/v1/video_status.get?video_id={video_id}",
                headers=self.headers
            )
            
            if response.status_code != 200:
                print(f"⚠️ Error checkeando estado: {response.text}")
                time.sleep(interval)
                continue
                
            data = response.json()
            status = data["data"]["status"]
            
            elapsed = int(time.time() - start_time)
            print(f"⏳ Estado HeyGen: {status} (Elapsed: {elapsed}s)")
            
            if status == "completed":
                url = data["data"]["video_url"]
                print(f"🎉 Video completado: {url}")
                return url
            elif status == "failed":
                 error = data["data"].get("error", "Error desconocido")
                 raise Exception(f"Falló el renderizado en HeyGen: {error}")
            
            time.sleep(interval)
            
        raise Exception("Timeout esperando a HeyGen")

    def download_video(self, url, local_path):
        """Descarga el video generado a una ruta local"""
        print(f"⬇️ Descargando video a {local_path}...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print("✅ Descarga completada")
            return local_path
        else:
            raise Exception(f"No se pudo descargar el video: {response.status_code}")
