from PIL import Image, ImageDraw

def create_inner_eye_mask(img: Image, box_size: int) -> Image:
    """
    Generate a mask highlighting the inner 3x3 modules of the QR code's position markers.

    Args:
        img (PIL.Image): The input QR code image (assumed to be square).
        box_size (int): Size of a single QR code module in pixels.

    Returns:
        PIL.Image: A grayscale mask image with the inner eye regions in white (255) and the rest in black (0).
    """
    img_size = img.size[0]
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)

    # Inner eyes are 3x3 modules, starting at (3, 3) offset
    offset = 6 * box_size
    size = 3 * box_size

    draw.rectangle((offset, offset, offset + size, offset + size), fill=255)  # top-left
    draw.rectangle((img_size - offset - size, offset, img_size - offset, offset + size), fill=255)  # top-right
    draw.rectangle((offset, img_size - offset - size, offset + size, img_size - offset), fill=255)  # bottom-left

    return mask


def create_outer_eye_mask(img: Image, box_size: int) -> Image:
    """
    Generate a mask highlighting the outer 7x7 modules of the QR code's position markers.

    Args:
        img (PIL.Image): The input QR code image (assumed to be square).
        box_size (int): Size of a single QR code module in pixels.

    Returns:
        PIL.Image: A grayscale mask image with the outer eye regions in white (255) and the rest in black (0).
    """
    img_size = img.size[0]
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)

    # Outer eyes are 7x7 modules, starting at (0, 0)
    outer_size = 7 * box_size
    inner_offset = 4 * box_size
    inner_size = 3 * box_size

    # Outer rectangles
    draw.rectangle((inner_offset, inner_offset, inner_offset + outer_size, inner_offset + outer_size), fill=255)  # top-left
    draw.rectangle((img_size - (inner_offset + outer_size), inner_offset, img_size - inner_offset, inner_offset + outer_size), fill=255)  # top-right
    draw.rectangle((inner_offset, img_size - (inner_offset + outer_size), (inner_offset + outer_size), img_size-inner_offset), fill=255)  # bottom-left

    return mask
