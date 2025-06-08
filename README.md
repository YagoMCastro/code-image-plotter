
# Code & Plot Renderer (ciplot)

This script takes a Python script file that contains `matplotlib` plotting code, executes it, and generates a combined image showing both the source code and the resulting plot side-by-side.

## Features

- Executes a Python script to generate a plot using `matplotlib`.
- Renders the script source code as an image.
- Combines the code image and the plot image horizontally.
- Saves the combined image to disk.

## Requirements

- Python 3.x
- `matplotlib`
- `Pillow` (PIL)
- Pygments

Install dependencies via pip if needed:

```bash
pip install matplotlib pillow
```

## Usage

```bash
python ciplot.py input_script.py output_image.png
```

- `input_script.py`: Path to the Python script with plotting code.
- `output_image.png`: Path to save the combined output image.

## How It Works

1. Reads the input Python script.
2. Executes the script while capturing the generated plot.
3. Converts the script text to an image.
4. Combines the code image and the plot image side-by-side.
5. Saves the combined image.

## Example

Given a script `plot_example.py` with matplotlib code:

```python
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Example Plot")
plt.show()
```

Run:

```bash
python ciplot.py plot_example.py output.png
```

The resulting `output.png` will display the code and its plot side-by-side.
