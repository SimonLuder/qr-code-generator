# QR Code Generator

A customizable Python QR code generator with support for logos, overlays, eye styling, and text annotations.

## Example Outputs

**Example 1**
```python
from pyqrcode.generator import QrCodeGenerator

QrCodeGenerator(
    data="AddYourUrlHere", 
    outfile="output/example1.png", 
).generate()
```

This generates the following output:
<div align="center">
  <img 
    src="output/example1.png" 
    alt="Example 1" 
    title="Example 1" 
    style="width: 30%; min-width: 200px; display: block; margin: 0 auto;"
  >
</div>

---

**Example 2**
```python
from pyqrcode.generator import QrCodeGenerator

QrCodeGenerator(
    data="https://github.com/SimonLuder",
    outfile="output/example2.png",
    logo="images/profile_img.png",
    sub_logo="images/github-mark.png",
    bar_style="Rounded",
    front_color=(255, 255, 255),
    back_color=(1, 1, 1),
    outer_eye_color=(210, 186, 132),
    inner_eye_color=(255, 226, 160),
    bottom_text="github.com/SimonLuder/qr-code-generator",
    bottom_text_color=(255, 255, 255),
    bottom_text_size=42,
    radius_ratio=0.1,
    box_size=30,
).generate()
```

This generates the following output:
<div align="center">
  <img 
    src="output/example2.png" 
    alt="Example 2" 
    title="Example 2" 
    style="width: 30%; min-width: 200px; display: block; margin: 0 auto;"
  >
</div>

---

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusernamqr-code-generator.git
   cd qr-code-generator
   ```

2. Install dependencies with:
    ```sh
    pip install -r requirements.txt
    ```

3. Edit `main.py` to customize your QR code parameters, then run:
    ```sh
    python main.py
    ```