from manim import *
import os

class IntroScene(Scene):
    def construct(self):
        title_text = os.getenv("MANIM_TEXT", "Bienvenidos")
        subtitle_text = os.getenv("MANIM_SUBTITLE", "Píldora Educativa")
        
        # Fondo transparente
        self.camera.background_color = None
        
        # Título grande
        title = Text(title_text, font_size=80, color=BLUE).to_edge(UP, buff=2)
        
        # Subtítulo
        subtitle = Text(subtitle_text, font_size=40, color=WHITE).next_to(title, DOWN)
        
        # Cuadro de fondo para el texto
        box = Rectangle(
            width=title.width + 1, 
            height=title.height + subtitle.height + 1,
            color=BLUE,
            fill_color=BLACK, 
            fill_opacity=0.7
        ).move_to(VGroup(title, subtitle).get_center())
        
        # Animación
        self.play(FadeIn(box), Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(VGroup(box, title, subtitle)))
