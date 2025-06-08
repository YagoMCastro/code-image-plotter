import sys
import os

if len(sys.argv) != 3:
        print("Usage: python ciplot.py input_script.py output_image.png")
        sys.exit(1)

script_path = sys.argv[1]
output_path = sys.argv[2]

if not os.path.exists(script_path):
    print(f"Error: File '{script_path}' not found.")
    sys.exit(1)