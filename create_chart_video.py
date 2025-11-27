"""
Script para crear videos animados de gráficas a partir de prompts de LLM
Flujo: LLM -> Generar datos/especificación -> Gráfica animada -> Video

Uso:
    python create_chart_video.py "Crea una gráfica de barras mostrando ventas por mes"
    python create_chart_video.py "Gráfica de líneas con crecimiento de usuarios" --model openai
    python create_chart_video.py "Pie chart de distribución de gastos" --duration 10
"""
import sys
import subprocess
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

# Intentar importar manim
_manim_imported = False
try:
    from manim import *
    import numpy as np
    _manim_imported = True
except ImportError:
    import numpy as np
    class Scene:
        pass
    class BarChart:
        pass
    class LineChart:
        pass
    class PieChart:
        pass
    class Axes:
        pass
    class Text:
        pass
    class VGroup:
        pass
    class Rectangle:
        pass
    class Dot:
        pass
    class VMobject:
        pass
    class Sector:
        pass
    BLUE = "#3498DB"
    RED = "#E74C3C"
    GREEN = "#2ECC71"
    YELLOW = "#F39C12"
    PURPLE = "#9B59B6"
    ORANGE = "#E67E22"
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    GRAY = "#95A5A6"
    UP = (0, 1, 0)
    DOWN = (0, -1, 0)
    LEFT = (-1, 0, 0)
    RIGHT = (1, 0, 0)
    PI = np.pi


class ChartAnimation(Scene):
    """Animación de gráfica profesional"""
    
    def construct(self):
        import base64
        
        # Leer configuración desde variables de entorno
        chart_data_encoded = os.environ.get('CHART_DATA', '')
        chart_type = os.environ.get('CHART_TYPE', 'bar')
        chart_title = os.environ.get('CHART_TITLE', 'Gráfica')
        duration_str = os.environ.get('CHART_DURATION', '10')
        
        # Decodificar datos del gráfico
        try:
            if chart_data_encoded:
                chart_data = json.loads(
                    base64.b64decode(chart_data_encoded.encode('ascii')).decode('utf-8')
                )
            else:
                chart_data = {}
        except:
            chart_data = {}
        
        try:
            duration = float(duration_str)
        except:
            duration = 10.0
        
        # Crear gráfica según el tipo
        if chart_type == 'bar':
            self._create_bar_chart(chart_data, chart_title, duration)
        elif chart_type == 'line':
            self._create_line_chart(chart_data, chart_title, duration)
        elif chart_type == 'pie':
            self._create_pie_chart(chart_data, chart_title, duration)
        else:
            self._create_bar_chart(chart_data, chart_title, duration)
    
    def _create_bar_chart(self, data: Dict, title: str, duration: float):
        """Crea una gráfica de barras animada"""
        # Configurar fondo
        self.camera.background_color = "#F5F5F5"
        
        # Extraer datos
        labels = data.get('labels', ['A', 'B', 'C', 'D', 'E'])
        values = data.get('values', [10, 20, 15, 25, 30])
        colors = data.get('colors', [BLUE, RED, GREEN, YELLOW, PURPLE])
        
        # Crear título
        title_text = Text(title, font_size=48, color=BLACK)
        title_text.to_edge(UP, buff=0.5)
        
        # Crear ejes y gráfica de barras
        max_value = max(values) if values else 10
        y_max = max_value * 1.2
        
        axes = Axes(
            x_range=[0, len(labels), 1],
            y_range=[0, y_max, max_value / 5],
            x_length=10,
            y_length=6,
            axis_config={"color": BLACK, "stroke_width": 2},
            tips=False,
        )
        axes.shift(DOWN * 0.5)
        
        # Crear barras usando Rectangle
        bars = VGroup()
        bar_width = 0.6
        
        for i, (label, value, color) in enumerate(zip(labels, values, colors)):
            # Crear barra como rectángulo
            bar = Rectangle(
                width=bar_width,
                height=(value / y_max) * axes.y_length,
                fill_opacity=0.8,
                fill_color=color,
                stroke_width=2,
                stroke_color=color
            )
            # Posicionar barra
            bar.move_to(axes.c2p(i + 0.5, value / 2))
            bars.add(bar)
            
            # Etiqueta del eje X
            label_text = Text(str(label), font_size=24, color=BLACK)
            label_text.move_to(axes.c2p(i + 0.5, -0.5))
            bars.add(label_text)
        
        # Animaciones
        self.play(FadeIn(title_text), run_time=0.5)
        self.wait(0.3)
        self.play(Create(axes), run_time=1.0)
        self.wait(0.3)
        
        # Animar barras una por una
        for i in range(len(labels)):
            self.play(Create(bars[i * 2]), run_time=0.4)
        
        # Mostrar valores en las barras
        value_labels = VGroup()
        for i, (value, color) in enumerate(zip(values, colors)):
            bar = bars[i * 2]
            value_text = Text(str(value), font_size=20, color=BLACK)
            value_text.move_to(bar.get_top() + UP * 0.2)
            value_labels.add(value_text)
        
        self.play(*[Write(label) for label in value_labels], run_time=1.0)
        
        # Pausa final
        self.wait(max(0, duration - 4.0))
        
        # Fade out
        self.play(
            FadeOut(title_text),
            FadeOut(axes),
            FadeOut(bars),
            FadeOut(value_labels),
            run_time=1.0
        )
    
    def _create_line_chart(self, data: Dict, title: str, duration: float):
        """Crea una gráfica de líneas animada"""
        self.camera.background_color = "#F5F5F5"
        
        labels = data.get('labels', ['Ene', 'Feb', 'Mar', 'Abr', 'May'])
        values = data.get('values', [10, 20, 15, 25, 30])
        color = data.get('color', BLUE)
        
        title_text = Text(title, font_size=48, color=BLACK)
        title_text.to_edge(UP, buff=0.5)
        
        max_value = max(values) if values else 10
        y_max = max_value * 1.2
        
        axes = Axes(
            x_range=[0, len(labels), 1],
            y_range=[0, y_max, max_value / 5],
            x_length=10,
            y_length=6,
            axis_config={"color": BLACK, "stroke_width": 2},
            tips=False,
        )
        axes.shift(DOWN * 0.5)
        
        # Crear puntos y etiquetas
        points = []
        label_texts = VGroup()
        for i, (label, value) in enumerate(zip(labels, values)):
            point = axes.c2p(i + 0.5, value)
            points.append(point)
            
            label_text = Text(str(label), font_size=24, color=BLACK)
            label_text.move_to(axes.c2p(i + 0.5, -0.5))
            label_texts.add(label_text)
        
        # Crear línea conectando puntos
        line_points = [axes.c2p(i + 0.5, values[i]) for i in range(len(values))]
        line = VMobject()
        line.set_points_as_corners(line_points)
        line.set_stroke(color=color, width=4)
        
        # Animaciones
        self.play(FadeIn(title_text), run_time=0.5)
        self.wait(0.3)
        self.play(Create(axes), run_time=1.0)
        self.play(*[Write(label) for label in label_texts], run_time=0.5)
        self.wait(0.3)
        self.play(Create(line), run_time=1.5)
        
        # Agregar puntos
        dots = VGroup(*[Dot(point, color=color, radius=0.08) for point in points])
        self.play(*[Create(dot) for dot in dots], run_time=1.0)
        
        # Valores
        value_labels = VGroup()
        for i, (point, value) in enumerate(zip(points, values)):
            value_text = Text(str(value), font_size=20, color=BLACK)
            value_text.move_to(point + UP * 0.3)
            value_labels.add(value_text)
        
        self.play(*[Write(label) for label in value_labels], run_time=1.0)
        self.wait(max(0, duration - 5.5))
        
        self.play(
            FadeOut(title_text),
            FadeOut(axes),
            FadeOut(line),
            FadeOut(dots),
            FadeOut(value_labels),
            FadeOut(label_texts),
            run_time=1.0
        )
    
    def _create_pie_chart(self, data: Dict, title: str, duration: float):
        """Crea una gráfica de pastel animada"""
        self.camera.background_color = "#F5F5F5"
        
        labels = data.get('labels', ['A', 'B', 'C', 'D'])
        values = data.get('values', [30, 25, 20, 25])
        colors = data.get('colors', [BLUE, RED, GREEN, YELLOW])
        
        title_text = Text(title, font_size=48, color=BLACK)
        title_text.to_edge(UP, buff=0.5)
        
        # Normalizar valores a porcentajes
        total = sum(values)
        if total == 0:
            total = 1
        percentages = [(v / total) * 100 for v in values]
        
        # Crear sectores del pastel usando Sector de Manim
        start_angle = 0
        sectors = VGroup()
        sector_labels = VGroup()
        
        for i, (label, value, pct, color) in enumerate(zip(labels, values, percentages, colors)):
            angle = (value / total) * 2 * PI
            
            sector = Sector(
                outer_radius=2,
                angle=angle,
                start_angle=start_angle,
                color=color,
                fill_opacity=0.8,
                stroke_width=2,
                stroke_color=WHITE
            )
            sectors.add(sector)
            
            # Etiqueta
            label_angle = start_angle + angle / 2
            label_pos = 2.5 * np.array([np.cos(label_angle), np.sin(label_angle), 0])
            label_text = Text(f"{label}\n{int(pct)}%", font_size=24, color=BLACK)
            label_text.move_to(label_pos)
            sector_labels.add(label_text)
            
            start_angle += angle
        
        # Animaciones
        self.play(FadeIn(title_text), run_time=0.5)
        self.wait(0.3)
        
        # Animar sectores uno por uno
        for sector in sectors:
            self.play(Create(sector), run_time=0.5)
        
        self.play(*[Write(label) for label in sector_labels], run_time=1.0)
        self.wait(max(0, duration - 3.0))
        
        self.play(
            FadeOut(title_text),
            FadeOut(sectors),
            FadeOut(sector_labels),
            run_time=1.0
        )


def call_llm(prompt: str, model: str = "openai") -> Dict[str, Any]:
    """
    Llama a un LLM para generar datos de gráfica
    
    Args:
        prompt: Prompt del usuario
        model: Modelo a usar (openai, anthropic, etc.)
    
    Returns:
        Dict con estructura: {
            'type': 'bar'|'line'|'pie',
            'title': str,
            'labels': List[str],
            'values': List[float],
            'colors': List[str] (opcional)
        }
    """
    try:
        if model == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
            
            system_prompt = """Eres un asistente que genera datos para gráficas. 
Responde SOLO con un JSON válido con esta estructura:
{
    "type": "bar" o "line" o "pie",
    "title": "Título descriptivo de la gráfica",
    "labels": ["Etiqueta1", "Etiqueta2", ...],
    "values": [valor1, valor2, ...],
    "colors": ["#color1", "#color2", ...] (opcional)
}

Ejemplos:
- Para ventas por mes: {"type": "bar", "title": "Ventas Mensuales", "labels": ["Ene", "Feb", "Mar"], "values": [100, 150, 120]}
- Para crecimiento: {"type": "line", "title": "Crecimiento de Usuarios", "labels": ["Q1", "Q2", "Q3"], "values": [1000, 1500, 2000]}
- Para distribución: {"type": "pie", "title": "Distribución de Gastos", "labels": ["Comida", "Transporte"], "values": [40, 60]}"""
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        elif model == "anthropic":
            from anthropic import Anthropic
            client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
            
            system_prompt = """Eres un asistente que genera datos para gráficas. 
Responde SOLO con un JSON válido con esta estructura:
{
    "type": "bar" o "line" o "pie",
    "title": "Título descriptivo de la gráfica",
    "labels": ["Etiqueta1", "Etiqueta2", ...],
    "values": [valor1, valor2, ...],
    "colors": ["#color1", "#color2", ...] (opcional)
}"""
            
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = message.content[0].text
            result = json.loads(content)
            return result
            
        else:
            raise ValueError(f"Modelo no soportado: {model}")
            
    except ImportError:
        print(f"[ERROR] Necesitas instalar el cliente para {model}")
        print(f"  pip install openai  # para OpenAI")
        print(f"  pip install anthropic  # para Anthropic")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Error al llamar al LLM: {e}")
        # Retornar datos de ejemplo
        return {
            "type": "bar",
            "title": "Gráfica de Ejemplo",
            "labels": ["A", "B", "C", "D", "E"],
            "values": [10, 20, 15, 25, 30],
            "colors": ["#3498DB", "#E74C3C", "#2ECC71", "#F39C12", "#9B59B6"]
        }


def render_chart_animation(chart_data: Dict, duration: float = 10.0, quality: str = "k"):
    """
    Renderiza la animación de gráfica
    
    Args:
        chart_data: Datos del gráfico (de call_llm)
        duration: Duración en segundos
        quality: Calidad de renderizado (l/m/h/k)
    """
    import base64
    
    # Codificar datos en base64
    chart_data_json = json.dumps(chart_data, ensure_ascii=False)
    chart_data_encoded = base64.b64encode(chart_data_json.encode('utf-8')).decode('ascii')
    
    os.environ['CHART_DATA'] = chart_data_encoded
    os.environ['CHART_TYPE'] = chart_data.get('type', 'bar')
    os.environ['CHART_TITLE'] = chart_data.get('title', 'Gráfica')
    os.environ['CHART_DURATION'] = str(duration)
    
    # Renderizar usando manim
    script_dir = Path(__file__).parent
    python_cmd = sys.executable
    
    cmd = [
        python_cmd,
        "-m", "manim",
        f"-pq{quality}",
        str(Path(__file__).absolute()),
        "ChartAnimation"
    ]
    
    print(f"[*] Renderizando animación de gráfica...")
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print(f"[OK] Animación completada!")
        script_name = Path(__file__).stem
        quality_folder = {
            "l": "480p15",
            "m": "720p30",
            "h": "1080p60",
            "k": "2160p60"
        }.get(quality, "2160p60")
        print(f"[OK] Video: media/videos/{script_name}/{quality_folder}/ChartAnimation.mp4")
    else:
        print()
        print(f"[ERROR] Error al renderizar")
    
    return result.returncode


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("=" * 60)
        print("Crear Video Animado de Gráfica desde LLM")
        print("=" * 60)
        print("\nUso:")
        print('  python create_chart_video.py "Crea una gráfica de barras de ventas por mes"')
        print('  python create_chart_video.py "Gráfica de líneas con crecimiento" --model openai')
        print('  python create_chart_video.py "Pie chart de distribución" --duration 12')
        print("\nOpciones:")
        print("  --model MODELO      Modelo LLM (openai, anthropic) - default: openai")
        print("  --duration N        Duración en segundos - default: 10")
        print("  --quality l|m|h|k   Calidad (k=4K máxima) - default: k")
        print("\nVariables de entorno:")
        print("  OPENAI_API_KEY      API key de OpenAI")
        print("  ANTHROPIC_API_KEY   API key de Anthropic")
        print("\n" + "=" * 60)
        sys.exit(1)
    
    prompt = sys.argv[1]
    model = "openai"
    duration = 10.0
    quality = "k"
    
    # Parsear argumentos
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--model" and i + 1 < len(sys.argv):
            model = sys.argv[i + 1]
            i += 2
        elif arg == "--duration" and i + 1 < len(sys.argv):
            try:
                duration = float(sys.argv[i + 1])
            except ValueError:
                print(f"[ERROR] Duración inválida: {sys.argv[i + 1]}")
                sys.exit(1)
            i += 2
        elif arg == "--quality" and i + 1 < len(sys.argv):
            quality = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    print("=" * 60)
    print("Creando gráfica animada desde LLM...")
    print("=" * 60)
    print(f"Prompt: {prompt}")
    print(f"Modelo: {model}")
    print(f"Duración: {duration} segundos")
    print(f"Calidad: {quality}")
    print("=" * 60)
    print()
    
    # Paso 1: Llamar al LLM
    print("[1/3] Llamando al LLM para generar datos de gráfica...")
    chart_data = call_llm(prompt, model)
    print(f"[OK] Gráfica generada: {chart_data.get('title', 'Sin título')}")
    print(f"     Tipo: {chart_data.get('type', 'bar')}")
    print(f"     Datos: {len(chart_data.get('labels', []))} elementos")
    print()
    
    # Paso 2: Renderizar animación
    print("[2/3] Creando animación...")
    render_chart_animation(chart_data, duration, quality)
    
    print()
    print("[3/3] ¡Completado!")

