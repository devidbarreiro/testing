import subprocess
import os

# Asegurar carpeta media
os.makedirs("media", exist_ok=True)

def create_dummy_video(filename, duration, color, text):
    """Crea un video mp4 simple con un color y texto usando FFmpeg"""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c={color}:s=1920x1080:d={duration}",
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", # Audio silencio
        "-vf", f"drawtext=text='{text}':fontcolor=white:fontsize=90:x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:v", "libx264", "-c:a", "aac", "-shortest",
        os.path.join("media", filename)
    ]
    subprocess.run(cmd)
    print(f"Creado: {filename}")

# 1. Crear el "HeyGen Mock" (Video base de 20 segundos)
# Simulamos que es el avatar hablando (fondo gris oscuro)
create_dummy_video("mock_heygen.mp4", 20, "gray", "AVATAR HEYGEN HABLANDO...")

print("Assets generados. Ahora puedes correr Django.")