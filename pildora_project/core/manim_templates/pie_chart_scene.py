from manim import *
import os
import json

class PieChartScene(Scene):
    def construct(self):
        # 1. Configuración de datos desde ENV
        data_json = os.getenv("MANIM_CHART_DATA", '{"labels": ["A", "B", "C"], "values": [30, 50, 20]}')
        chart_title = os.getenv("MANIM_CHART_TITLE", "Distribución")
        
        try:
            data = json.loads(data_json)
            labels = data.get("labels", [])
            values = data.get("values", [])
            if not values: raise ValueError("No values")
        except:
            labels = ["Error"]
            values = [1]
            
        # 2. Configuración Visual
        self.camera.background_color = WHITE 
        
        # 3. Crear Gráfico MANUALMENTE (Sectors)
        total = sum(values)
        start_angle = 90 * DEGREES
        
        sectors = VGroup()
        labels_group = VGroup()
        
        colors = [BLUE, TEAL, GREEN, MAROON, PURPLE, ORANGE]
        
        current_angle = start_angle
        
        for i, (val, label_text) in enumerate(zip(values, labels)):
            portion = val / total
            angle = portion * 360 * DEGREES
            
            # Sector
            sector = AnnularSector(
                outer_radius=2.5, 
                inner_radius=0, 
                start_angle=current_angle, 
                angle=-angle, # Clockwise
                fill_color=colors[i % len(colors)], 
                fill_opacity=1, 
                stroke_width=2, 
                stroke_color=WHITE
            )
            sectors.add(sector)
            
            # Etiqueta (Posicionada en el ángulo medio)
            mid_angle = current_angle - (angle / 2)
            label_radius = 2.8 # Un poco fuera del sector
            
            # Coordenadas polares a cartesianas
            x = label_radius * np.cos(mid_angle)
            y = label_radius * np.sin(mid_angle)
            
            pct_text = f"{int(portion*100)}%"
            full_text = f"{label_text}\n{pct_text}"
            
            lbl = Text(full_text, font_size=24, color=BLACK, line_spacing=1)
            lbl.move_to([x, y, 0])
            
            # Ajustar alineación: Usamos coordenadas polares calculadas
            lbl.move_to([x, y, 0])
            
            labels_group.add(lbl)
            
            current_angle -= angle

        # Agrupar todo y centrar (desplazado a la izquierda para dejar sitio al avatar PIP)
        chart_group = VGroup(sectors, labels_group)
        chart_group.move_to(LEFT * 2)

        # 4. Título
        title = Text(chart_title, font_size=40, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        title.set_x(chart_group.get_x())
        
        # 5. Animación
        self.play(Write(title))
        self.play(Create(sectors), run_time=1.5)
        self.play(FadeIn(labels_group))
        self.wait(1)
