from manim import *
import os
import json

class BulletListScene(Scene):
    def construct(self):
        # 1. Configuración de datos desde ENV
        items_json = os.getenv("MANIM_LIST_ITEMS", '["Punto 1", "Punto 2", "Punto 3"]')
        title_text = os.getenv("MANIM_LIST_TITLE", "Claves Principales")
        
        try:
            items = json.loads(items_json)
        except:
            items = ["Error en datos"]
            
        # 2. Configuración Visual
        self.camera.background_color = WHITE 
        
        # 3. Título
        title = Text(title_text, font_size=48, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=1)
        
        # 4. Lista
        bullet_list = VGroup()
        for i, item_text in enumerate(items):
            dot = Dot(color=BLUE)
            text = Text(item_text, font_size=36, color=BLACK)
            line = VGroup(dot, text).arrange(RIGHT, buff=0.5)
            bullet_list.add(line)
            
        bullet_list.arrange(DOWN, buff=0.5, align_edge=LEFT)
        bullet_list.next_to(title, DOWN, buff=1)
        
        # 5. Animación
        self.play(Write(title))
        self.play(FadeIn(bullet_list, shift=dict(direction=DOWN, magnitude=0.5)), run_time=1.5)
        self.wait(1)
