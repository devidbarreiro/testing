from manim import *
import os
import json

class BarChartScene(Scene):
    def construct(self):
        # 1. Configuración de datos desde ENV
        data_json = os.getenv("MANIM_CHART_DATA", '{"labels": ["A", "B", "C"], "values": [3, 5, 2]}')
        chart_title = os.getenv("MANIM_CHART_TITLE", "Estadísticas")
        
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
        
        # 3. Crear Gráfico MANUALMENTE (Sin LaTeX)
        max_val = max(values)
        chart_height = 5
        chart_width = 8
        
        # Ejes
        x_axis = Line(start=ORIGIN, end=RIGHT * chart_width, color=BLACK, stroke_width=4)
        y_axis = Line(start=ORIGIN, end=UP * chart_height, color=BLACK, stroke_width=4)
        axes = VGroup(x_axis, y_axis).to_edge(DL, buff=1.5)
        
        # Barras y Etiquetas
        bars = VGroup()
        x_labels = VGroup()
        
        bar_count = len(values)
        bar_width = (chart_width / bar_count) * 0.6
        spacing = (chart_width / bar_count) * 0.4
        
        colors = [BLUE, TEAL, GREEN, MAROON, PURPLE]
        
        for i, (val, label_text) in enumerate(zip(values, labels)):
            # Altura relativa
            height = (val / max_val) * chart_height
            
            bar = Rectangle(height=height, width=bar_width, fill_color=colors[i % len(colors)], fill_opacity=1, stroke_width=0)
            # Posicionar barra: Start at axis start + spacing + width/2
            x_pos = (i * (bar_width + spacing)) + spacing + (bar_width / 2)
            bar.move_to(axes.get_corner(DL) + RIGHT * x_pos + UP * (height / 2))
            
            bars.add(bar)
            
            # Etiqueta X
            lbl = Text(str(label_text), font_size=24, color=BLACK)
            lbl.next_to(bar, DOWN, buff=0.2)
            x_labels.add(lbl)
            
            # Etiqueta Valor (opcional, encima de barra)
            val_lbl = Text(str(val), font_size=20, color=BLACK)
            val_lbl.next_to(bar, UP, buff=0.1)
            bars.add(val_lbl)

        # 4. Título
        title = Text(chart_title, font_size=40, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        title.set_x(axes.get_center()[0] + 1) # Centrar respecto al gráfico aprox
        
        # 5. Animación
        self.play(Write(title), Create(axes))
        self.play(img.animate.set_height(img.height) for img in bars) # Animación simple de aparición o FadeIn
        # Mejor animación para barras: GrowFromEdge(bar, DOWN)
        
        anims = [GrowFromEdge(bar, DOWN) for bar in bars if isinstance(bar, Rectangle)]
        txt_anims = [FadeIn(lbl) for lbl in x_labels]
        val_anims = [FadeIn(lbl) for lbl in bars if isinstance(lbl, Text)]
        
        self.play(*anims, *txt_anims, *val_anims, run_time=1.5)
        self.wait(1)
