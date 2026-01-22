from manim import *
import os

class InfografiaTexto(Scene):
    def construct(self):
        # Leemos el texto que nos pasa Django
        texto_mostrar = os.getenv("MANIM_TEXT", "Infografía Genérica")
        
        # Fondo transparente para el overlay
        self.camera.background_color = None 
        
        # Creamos un panel estilo "Noticias"
        panel = Rectangle(width=10, height=3, color=BLUE, fill_opacity=0.8).to_edge(DOWN)
        texto = Text(texto_mostrar, font_size=48).move_to(panel.get_center())
        
        self.play(FadeIn(panel, shift=UP), Write(texto))
        self.wait(2)