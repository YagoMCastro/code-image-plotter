import sys
import os
import io
from PIL import Image
import matplotlib.pyplot as plt

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

def fake_show(*args, **kwargs):
    pass

def render_plot_from_code(code_str):
    plt.show = fake_show
    plt.close('all')

    global_namespace = {"plt": plt, "show": fake_show}
    local_namespace = {}

    exec(code_str, global_namespace, local_namespace)

    fig = plt.gcf()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

def render_code_image_colored(code_str, font_size=16, style='monokai'):
    formatter = ImageFormatter(font_name='DejaVu Sans Mono', font_size=font_size, style=style, line_numbers=False)
    lexer = PythonLexer()
    img_data = highlight(code_str, lexer, formatter)

    buf = io.BytesIO(img_data)
    img = Image.open(buf)
    return img

def combine_images(code_img, plot_img):
    if plot_img.height < code_img.height:
        scale_factor = code_img.height / plot_img.height
        new_width = int(plot_img.width * scale_factor)
        plot_img = plot_img.resize((new_width, code_img.height), resample=Image.LANCZOS)

    height = max(code_img.height, plot_img.height)
    combined = Image.new("RGB", (code_img.width + plot_img.width, height), "white")
    combined.paste(code_img, (0, 0))
    combined.paste(plot_img, (code_img.width, 0))
    return combined

if len(sys.argv) != 3:
    print("Usage: python ciplot.py input_script.py output_image.png")
    sys.exit(1)

script_path = sys.argv[1]
output_path = sys.argv[2]

if not os.path.exists(script_path):
    print(f"Error: File '{script_path}' not found.")
    sys.exit(1)

with open(script_path, "r") as f:
    code_str = f.read()

try:
    plot_img = render_plot_from_code(code_str)
except Exception as e:
    print("Error executing code:", e)
    sys.exit(1)

code_img = render_code_image_colored(code_str)
combined_img = combine_images(code_img, plot_img)

combined_img.save(output_path)
print(f"✅ Image saved as {output_path}")
