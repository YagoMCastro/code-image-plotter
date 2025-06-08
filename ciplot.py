import sys
import os
import io
from PIL import Image
import matplotlib.pyplot as plt

def render_plot_from_code(code_str):
    global_namespace = {}
    local_namespace = {}
    exec(code_str, global_namespace, local_namespace)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return Image.open(buf)

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