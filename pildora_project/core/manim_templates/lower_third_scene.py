from manim import *
import os

class LowerThirdScene(Scene):
    def construct(self):
        # 1. Configuración de datos
        title_text = os.getenv("MANIM_LOWER_TITLE", "Tema Principal")
        name_text = os.getenv("MANIM_LOWER_NAME", "Avatar IA")
        
        # 2. Configuración Visual
        # Fondo transparente para superponer
        self.camera.background_color = None 
        
        # 3. Creación de Elementos
        bar = RoundedRectangle(corner_radius=0.2, height=1.5, width=8, color=BLUE_E, fill_opacity=0.9)
        bar.to_corner(DL, buff=1)
        
        # Textos
        title = Text(title_text, font_size=36, color=WHITE, weight=BOLD)
        name = Text(name_text, font_size=24, color=LIGHT_GREY)
        
        # Agrupar y posicionar textos dentro de la barra
        text_group = VGroup(title, name).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        text_group.move_to(bar.get_center())
        
        group = VGroup(bar, text_group)
        
        # 4. Animación
        self.play(FadeIn(bar, shift=RIGHT), Write(title), FadeIn(name, shift=UP), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(group, shift=LEFT), run_time=1)
