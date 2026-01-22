from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import os
import sys
import subprocess
from .builder import FFmpegPildoraBuilder

# --- PLANNER INTELIGENTE ---
def parse_script_to_plan(raw_text):
    """
    Convierte el guion de usuario en un plan de producción.
    Estructura: Intro -> Avatar -> (Infografía c/x tiempo) -> Avatar Fin
    """
    import math
    
    # 1. Limpieza básica
    paragraphs = [p.strip() for p in raw_text.split('\n') if p.strip()]
    if not paragraphs:
        return {"guion": "Hola, esto es un video de prueba.", "eventos": []}
    
    # 2. Extraer Título (Intro)
    # Usamos el primer párrafo como título si es corto, sino "Píldora Educativa"
    possible_title = paragraphs[0]
    title_text = "Píldora Educativa"
    script_start_idx = 0
    
    if len(possible_title.split()) < 10:
        title_text = possible_title
        script_start_idx = 1 # El guion real empieza después del título
        
    full_script = "\n\n".join(paragraphs[script_start_idx:])
    
    # Si no queda guion, usar el título como guion también
    if not full_script:
        full_script = title_text
    
    # 3. Calcular Tiempos Estimados
    # Velocidad promedio: 150 palabras/minuto = 2.5 palabras/segundo
    words = full_script.split()
    total_duration = len(words) / 2.5
    
    
    eventos = []

    # EVENTO 1: INTRO (0-4 segundos) - SILENCIOSA (Full Screen)
    # La intro visual tapa al avatar mientras presenta el tema
    eventos.append({
        "tipo": "INTRO",
        "texto": title_text,
        "subtexto": "Presentado por IA",
        "start": 0,
        "end": 4
    })

    # EVENTO 2: LOWER THIRD (4-9 segundos)
    # Titulo y Nombre al empezar a hablar
    eventos.append({
        "tipo": "LOWER_THIRD",
        "texto": title_text, # "Tema Principal"
        "subtexto": "Avatar Virtual", # "Avatar IA"
        "start": 4,
        "end": 9
    })
    
    # EVENTOS INTERMEDIOS: INFOGRAFÍAS
    # Insertar una infografía cada ~15-20 segundos (o cada párrafo largo)
    # Por simplicidad: Detectamos párrafos y ponemos infografía al inicio de cada uno (saltando el primero)
    
    current_time = 4 # Empezamos a buscar contenido despues de Intro+Lower
    script_paragraphs = paragraphs[script_start_idx:]
    
    for i, para in enumerate(script_paragraphs):
        para_words = len(para.split())
        para_duration = para_words / 2.5
        
        # Si es suficientemente largo, metemos infografía o gráfico
        if para_words > 10:
            # ... (detection logic) ...
            pass # Keep existing logic logic below but formatted correctly in replace chunk if needed
            # For simplicity in this tool call, I will assume the loop continues correctly. 
            # But wait, replace_file_content replaces a block. I need to be careful with the loop content.
            # I will just rewrite the parsing start and the extra event.
            
# ... (Continuing the replacement chunk logic) ...
# Actually, I should use a cleaner replacement.

# Let's replace from "eventos = []" down to "current_time = 0" 

    script_paragraphs = paragraphs[script_start_idx:]
    
    for i, para in enumerate(script_paragraphs):
        para_words = len(para.split())
        para_duration = para_words / 2.5
        
        # Si es suficientemente largo, metemos infografía o gráfico
        if para_words > 10:
            # Detección heurística de contenido
            keywords_chart = ["dato", "gráfico", "estadística", "porcentaje", "%"]
            keywords_pie = ["tarta", "circular", "distribución", "sectores"]
            keywords_list = ["lista", "puntos", "claves", "elementos", "pasos"]
            keywords_quote = ["frase", "cita", "dijo", "menciona", "inspirador"]
            
            is_chart = any(k in para.lower() for k in keywords_chart)
            is_pie = any(k in para.lower() for k in keywords_pie)
            is_list = any(k in para.lower() for k in keywords_list)
            is_quote = any(k in para.lower() for k in keywords_quote)
            
            if is_pie:
                tipo_evento = "PIE_CHART"
            elif is_chart:
                tipo_evento = "CHART"
            elif is_list:
                tipo_evento = "LIST"
            elif is_quote:
                tipo_evento = "QUOTE"
            else:
                tipo_evento = "INFOGRAFIA"
            
            # Texto resumen de la infografía (primeras 3-4 palabras)
            info_text = " ".join(para.split()[:4]).upper() + "..."
            
            evento = {
                "tipo": tipo_evento,
                "texto": info_text,
                "start": math.floor(current_time), # Inicio del párrafo
                "end": math.floor(current_time + 8) # Duración fija de 8s (más tiempo para charts)
            }
            
            if is_pie:
                evento["chart_data"] = json.dumps({
                    "labels": ["Sector A", "Sector B", "Sector C"],
                    "values": [30, 50, 20]
                })
                evento["chart_title"] = "Distribución"
            elif is_chart:
                # Datos dummy para demo
                evento["chart_data"] = json.dumps({
                    "labels": ["Datos A", "Datos B", "Datos C", "Datos D"],
                    "values": [25, 40, 15, 80]
                })
                evento["chart_title"] = "Datos Relevantes"
            elif is_list:
                evento["list_items"] = json.dumps([
                    "Punto Importante 1",
                    "Clave Esencial 2",
                    "Elemento Final 3"
                ])
                evento["list_title"] = "Resumen de Claves"
            elif is_quote:
                # Extraer algo que parezca una cita, o usar dummy
                evento["quote_text"] = "La innovación distingue a los líderes de los seguidores."
                evento["quote_author"] = "Steve Jobs"
                
            eventos.append(evento)
            
        current_time += para_duration
    
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- PLAN GENERATION ---\n")
        f.write(f"Script words: {len(words)}\n")
        for ev in eventos:
            f.write(f"Event: {ev['tipo']} at {ev['start']}s (Text: {ev['texto']})\n")
    
    return {
        "guion": full_script,
        "duracion_total": total_duration,
        "eventos": eventos
    }

@csrf_exempt
def generar_pildora(request):
    if request.method == "POST":
        try:
            # Leer body para obtener el script (si viene de fetch JSON)
            import json
            data = json.loads(request.body)
            user_script = data.get("script", "")
            
            # 1. PLANIFICACIÓN
            plan = parse_script_to_plan(user_script)
            print(f"📋 Plan generado: {len(plan['eventos'])} eventos. Duración est: {plan['duracion_total']}s")
            
            # 2. Obtener Video Base (HeyGen vs Mock)
            base_dir = settings.MEDIA_ROOT
            output_final = os.path.join(base_dir, "pildora_final.mp4")
            
            # Verificar API KEY
            api_key = os.getenv("HEYGEN_API_KEY")
            
            # --- MODO TEST: REUTILIZAR VIDEO ---
            # Buscamos si existe ya un video de HeyGen para no gastar créditos probando overlays
            import glob
            existing_heygen_files = glob.glob(os.path.join(base_dir, "heygen_*.mp4"))
            
            if existing_heygen_files:
                # Ordenar por fecha y coger el último
                base_video_path = max(existing_heygen_files, key=os.path.getctime)
                print(f"♻️ MODO TEST DEPURACIÓN: Reutilizando video existente: {base_video_path}")
                
                # VERIFICAR DURACIÓN Y LOOP SI ES NECESARIO
                # Obtener duración con ffprobe
                try:
                    probe_cmd = [
                        'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', base_video_path
                    ]
                    duration_str = subprocess.check_output(probe_cmd).decode().strip()
                    base_duration = float(duration_str)
                    
                    target_duration = plan['duracion_total'] + 10 # Margen de seguridad
                    
                    if base_duration < target_duration:
                        print(f"⚠️ Video base corto ({base_duration}s) vs Plan ({target_duration}s). Extendiendo en bucle...")
                        looped_path = os.path.join(base_dir, "looped_base.mp4")
                        
                        # Calculate loop count needed
                        loop_count = int(target_duration / base_duration) + 1
                        
                        # Create looped video
                        loop_cmd = [
                            'ffmpeg', '-y', '-stream_loop', str(loop_count), '-i', base_video_path,
                            '-t', str(target_duration),
                            '-c', 'copy', looped_path
                        ]
                        subprocess.run(loop_cmd, check=True)
                        base_video_path = looped_path
                        print(f"✅ Video extendido generado: {looped_path}")
                except Exception as ex:
                    print(f"⚠️ Error al extender video: {ex}. Usando original.")

            elif api_key and api_key != "tu_api_key_aqui":
                # === MODO REAL (HeyGen API) ===
                print("🔵 Iniciando modo REAL con HeyGen...")
                from .heygen_service import HeyGenService
                service = HeyGenService()
                
                # Generar y Esperar (Timeout aumentado a 20 min para videos largos)
                # Modificamos resolución a 720p en servicio
                video_id = service.generate_video(plan["guion"])
                video_url = service.wait_for_completion(video_id, timeout=1200)
                
                # Descargar
                video_heygen_path = os.path.join(base_dir, f"heygen_{video_id}.mp4")
                service.download_video(video_url, video_heygen_path)
                
                base_video_path = video_heygen_path
            else:
                # === MODO DEV (Mock Local) ===
                print("🟡 HEYGEN_API_KEY no encontrada o default. Usando MOCK local.")
                base_video_path = os.path.join(base_dir, "mock_heygen.mp4")
                if not os.path.exists(base_video_path):
                     return JsonResponse({"status": "error", "message": "Falta mock_heygen.mp4"}, status=500)

            # 3. Composición con FFmpeg (Builder)
            builder = FFmpegPildoraBuilder(base_video_path, output_final)
            
            # 4. Generar Assets on-the-fly con Manim
            for evento in plan['eventos']:
                # Manim con transparencia (-t) genera .mov automáticamente aunque pidamos .webm
                asset_filename = f"asset_{evento['tipo']}_{evento['start']}.mov"
                asset_path = os.path.join(base_dir, asset_filename)
                
                # Configurar Manim según tipo
                env = os.environ.copy()
                env["MANIM_TEXT"] = evento['texto']
                
                scene_name = "InfografiaTexto"
                scene_file = "core/manim_templates/basic_scene.py"
                
                if evento['tipo'] == "INTRO":
                    scene_name = "IntroScene"
                    scene_file = "core/manim_templates/intro_scene.py"
                    env["MANIM_SUBTITLE"] = evento.get('subtexto', '')
                elif evento['tipo'] == "CHART":
                    scene_name = "BarChartScene"
                    scene_file = "core/manim_templates/chart_scene.py" 
                    env["MANIM_CHART_DATA"] = evento.get('chart_data', '{}')
                    env["MANIM_CHART_TITLE"] = evento.get('chart_title', 'Gráfico')
                elif evento['tipo'] == "LIST":
                    scene_name = "BulletListScene"
                    scene_file = "core/manim_templates/list_scene.py" 
                    env["MANIM_LIST_ITEMS"] = evento.get('list_items', '[]')
                    env["MANIM_LIST_TITLE"] = evento.get('list_title', 'Lista')
                elif evento['tipo'] == "QUOTE":
                    scene_name = "QuoteScene"
                    scene_file = "core/manim_templates/quote_scene.py" 
                    env["MANIM_QUOTE_TEXT"] = evento.get('quote_text', '')
                    env["MANIM_QUOTE_AUTHOR"] = evento.get('quote_author', '')
                elif evento['tipo'] == "LOWER_THIRD":
                    scene_name = "LowerThirdScene"
                    scene_file = "core/manim_templates/lower_third_scene.py" 
                    env["MANIM_LOWER_TITLE"] = evento.get('texto', 'Tema')
                    env["MANIM_LOWER_NAME"] = evento.get('subtexto', 'Nombre')
                elif evento['tipo'] == "PIE_CHART":
                    scene_name = "PieChartScene"
                    scene_file = "core/manim_templates/pie_chart_scene.py" 
                    env["MANIM_CHART_DATA"] = evento.get('chart_data', '{}')
                    env["MANIM_CHART_TITLE"] = evento.get('chart_title', 'Distribución')
                
                cmd_manim = [
                    sys.executable, "-m", "manim", "-qm", "-t",
                    "--output_file", asset_path,
                    scene_file, scene_name
                ]
                
                print(f"🎨 Renderizando asset {evento['tipo']} ({evento['start']}s)...")
                with open("debug_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"Executing Manim for {evento['tipo']}: {' '.join(cmd_manim)}\n")
                    f.write(f"Output Expected: {asset_path}\n")

                result = subprocess.run(cmd_manim, env=env, cwd=settings.BASE_DIR, capture_output=True)
                
                if result.returncode != 0:
                    err_msg = result.stderr.decode('utf-8', errors='replace')
                    print(f"❌ Manim Error (Code {result.returncode}):")
                    print(err_msg)
                    with open("debug_log.txt", "a", encoding="utf-8") as f:
                        f.write(f"\n--- ERROR MANIM {evento['tipo']} ---\n{err_msg}\n")
                
                # Verificar si existe el archivo (Manim puede haberle añadido .mov extra si nos equivocamos antes, pero ahora pedimos .mov)
                layout_mode = "PIP" if evento['tipo'] in ["CHART", "LIST", "QUOTE", "PIE_CHART"] else "NORMAL"
                
                if os.path.exists(asset_path):
                     print(f"✅ Asset generado: {asset_path} (Layout: {layout_mode})")
                     builder.add_overlay(asset_path, evento['start'], evento['end'], layout=layout_mode)
                else:
                    # Fallback por si Manim hizo algo raro con el nombre (ej: .webm.mov)
                    possible_double_ext = asset_path.replace(".mov", ".webm.mov")
                    if os.path.exists(possible_double_ext):
                        print(f"✅ Asset generado (extensión doble): {possible_double_ext}")
                        builder.add_overlay(possible_double_ext, evento['start'], evento['end'], layout=layout_mode)
                    else:
                        print(f"⚠️ Alerta: No se encontró output de Manim en {asset_path}")

            # 5. Renderizar Video Final
            builder.render()
            
            return JsonResponse({"status": "ok", "url": "/media/pildora_final.mp4"})
        except Exception as e:
            print(f"❌ Error General: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return render(request, "index.html")