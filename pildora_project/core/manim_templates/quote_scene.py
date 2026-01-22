from manim import *
import os

class QuoteScene(Scene):
    def construct(self):
        # 1. Datos
        quote_text = os.getenv("MANIM_QUOTE_TEXT", "La imaginación es más importante que el conocimiento.")
        author_text = os.getenv("MANIM_QUOTE_AUTHOR", "Albert Einstein")
        
        # 2. Visual
        self.camera.background_color = WHITE
        
        # 3. Elementos
        quote = Text(f'"{quote_text}"', font_size=40, color=BLACK, slant=ITALIC, line_spacing=1.2)
        quote.set_preserve_aspect_ratio(True) # Ensure text doesn't stretch weirdly
        quote.width = 10 # Width limit roughly
        
        author = Text(f"- {author_text}", font_size=32, color=GREY, weight=BOLD)
        author.next_to(quote, DOWN, buff=0.5, aligned_edge=RIGHT)
        
        group = VGroup(quote, author).move_to(ORIGIN)
        
        # 4. Animación
        self.play(Write(quote), run_time=2)
        self.play(FadeIn(author, shift=UP))
        self.wait(1)
