from PIL import ImageDraw, ImageFont
from matplotlib import font_manager

def add_text_to_image(image, text, width_ratio, height_ratio, text_color=(255, 255, 255), font_path=None, font_size=42):
    """
    Adds centered text to a PIL image at a proportional position.
    """
    draw = ImageDraw.Draw(image)

    font = load_font(font_path, font_size)

    img_width, img_height = image.size
    x = int(img_width * width_ratio)
    y = int(img_height * height_ratio)

    # Calculate text size using textbbox (Pillow ≥10.0)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Adjust position to center the text
    position = (x - text_width // 2, y - text_height // 2)

    # Draw text
    draw.text(position, text, fill=text_color, font=font)

    return image


def load_font(font_path=None, size=42):

    if not isinstance(size, int) or size <= 0:
        raise ValueError("Font size must be a positive integer")

    try:
        return ImageFont.truetype(font_path, size)
    except:
        print("Loading default font")
        return ImageFont.load_default(size)
        

def get_system_fonts():
    all_fonts = {font.name.lower(): font.fname for font in font_manager.fontManager.ttflist}
    return all_fonts