import sys
import os
import io
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

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

def render_code_image(code_str, width=500, font_size=16):
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    code_lines = code_str.strip().splitlines()
    line_height = font.getbbox("A")[3] - font.getbbox("A")[1] + 4
    img_height = line_height * len(code_lines) + 20

    img = Image.new("RGB", (width, img_height), color="white")
    draw = ImageDraw.Draw(img)

    for i, line in enumerate(code_lines):
        draw.text((10, i * line_height + 10), line, font=font, fill="black")

    return img

def combine_images(code_img, plot_img):
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

code_img = render_code_image(code_str)
combined_img = combine_images(code_img, plot_img)

combined_img.save(output_path)
print(f"✅ Image saved as {output_path}")
