import subprocess
import os

class FFmpegPildoraBuilder:
    def __init__(self, base_video, output_path):
        self.base_video = base_video
        self.output_path = output_path
        self.overlays = []
    def add_overlay(self, video_path, start, end, layout="NORMAL"):
        """Añade una capa visual (infografía) en un intervalo de tiempo"""
        self.overlays.append({
            "path": video_path,
            "start": start,
            "end": end,
            "layout": layout
        })

    def render(self):
        # 1. Inputs: El primero siempre es el base (HeyGen)
        cmd = ['ffmpeg', '-y', '-i', self.base_video]
        
        # Añadimos los inputs de las superposiciones
        for overlay in self.overlays:
            cmd.extend(['-i', overlay['path']])

        # 2. Filter Complex: La magia de las capas
        filter_chain = []
        # However, filter chains are linear. We can create the PIP component inside the loop or globally.
        # To avoid complex splitting management, we'll assume we can reference [0:v] again relative to time?
        # No, filters operate on streams.
        
        # Helper to get pip filter
        def get_pip_layer(input_idx, overlay_tag):
             # Returns filters to put avatar on top of overlay
             # We take [0:v] (base), scale it, and put it on [input_idx]
             # BUT [0:v] is a stream. Cloning it for every overlay is tricky in pure filter_complex linear definition without splits.
             pass

        # REWRITE OF FILTER LOGIC
        # 1. Start with [0:v] as initial `last_output`.
        # 2. For each overlay:
        #    - If Normal: [last_output][new_overlay]overlay...
        #    - If PIP: 
        #      We need to construct a "Composed Frame": [Chart] + [MiniAvatar].
        #      Then overlay [Composed Frame] on top of [last_output].
        #      To get [MiniAvatar], we take [0:v] and scale it.
        #      Issue: [0:v] is a continuous stream. sync is maintained.
        #      So: [0:v]split[main][copy_for_pip]; [copy_for_pip]scale=...[mini_avatar]
        #      Then [Chart][mini_avatar]overlay... -> [composed_chart]
        #      Then [main][composed_chart]overlay... -> [out]
        
        # Let's try to implement this logic dynamically.
        
        # Initialize splits if we have PIP events
        has_pip = any(o.get('layout') == 'PIP' for o in self.overlays)
        
        cmd_filters = []
        if has_pip:
            # Create a dedicated PIP stream from 0:v that runs parallel?
            # Actually easier: Just simply put [0:v] into the pip scaler every time? 
            # FFmpeg allows reusing input label? Yes, typically [0:v] can be fed to multiple filters if split is auto-inserted or we do it.
            # Let's do explicit split to be safe/clear.
            
            # Count how many times we need 0:v (1 for base + N for PIPs)
            pip_count = sum(1 for o in self.overlays if o.get('layout') == 'PIP')
            split_outputs = ["[v_main]"] + [f"[v_pip_src_{i}]" for i in range(pip_count)]
            cmd_filters.append(f"[0:v]split={len(split_outputs)}{''.join(split_outputs)}")
            last_output = "[v_main]"
            pip_usage_idx = 0
        else:
            last_output = "[0:v]"

        for i, overlay in enumerate(self.overlays):
            input_idx = i + 1
            layout = overlay.get('layout', 'NORMAL')
            
            # Prepare the overlay video (scale to 720p)
            cmd_filters.append(
                f"[{input_idx}:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720[ovr_{input_idx}_scaled]"
            )
            
            overlay_ref = f"[ovr_{input_idx}_scaled]"

            if layout == 'PIP':
                # Create the PIP composition
                # 1. Take one of the split PIP sources
                pip_src = f"[v_pip_src_{pip_usage_idx}]"
                pip_usage_idx += 1
                
                # 2. Scale it to 400x400 (square for circle) and add transparency
                # We force scale to 400:400 to ensure it's square for the circle mask
                # Then use geq to create the circle alpha mask
                cmd_filters.append(
                    f"{pip_src}scale=400:400:force_original_aspect_ratio=decrease,pad=400:400:-1:-1:color=black@0,format=yuva420p,"
                    f"geq=lum='p(X,Y)':a='if(lte(pow(X-W/2,2)+pow(Y-H/2,2),pow(W/2-10,2)),255,0)'[pip_img_{i}]"
                )
                
                # 3. Overlay PIP onto the Chart (Chart is background)
                # Bottom-Right: W-w-20 : H-h-20
                cmd_filters.append(
                    f"{overlay_ref}[pip_img_{i}]overlay=main_w-overlay_w-30:main_h-overlay_h-30[composed_{i}]"
                )
                overlay_ref = f"[composed_{i}]"
            
            # Apply to main timeline
            next_output = f"v_out_{input_idx}"
            cmd_filters.append(
                f"{last_output}{overlay_ref}overlay=0:0:enable='between(t,{overlay['start']},{overlay['end']})'[{next_output}]"
            )
            last_output = f"[{next_output}]"

        full_filter = ";".join(cmd_filters)
        
        # Si no hay overlays, solo copiamos, si hay, aplicamos filtro
        if self.overlays:
            cmd.extend(['-filter_complex', full_filter, '-map', last_output])
        else:
            cmd.extend(['-map', '0:v'])

        # 3. Audio y Salida: Usamos SIEMPRE el audio del base (0:a)
        # IMPLEMENTACIÓN "SILENT INTRO": Silenciar audio los primeros 4 segundos via afade/volume
        cmd.extend([
            '-map', '0:a', 
            '-af', "volume=0:enable='between(t,0,4)'", # Mutea primeros 4s
            '-c:v', 'libx264', '-preset', 'ultrafast', # Rápido para pruebas
            '-c:a', 'aac', # Re-encode audio to apply filter
            self.output_path
        ])

        print("Renderizando Píldora...")
        subprocess.run(cmd, check=True)
        return self.output_path