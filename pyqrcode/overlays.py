from PIL import Image


def add_overlay_icon(
    qr_image: Image.Image,
    icon_path: str,
    position_ratio: tuple[float, float] = (0.5, 0.5),
    scale_ratio: float = 0.1
    ) -> Image.Image:
    """
    Adds an overlay PNG icon on top of the QR image at a proportional position and scale.

    :param qr_image: PIL Image of the QR code
    :param icon_path: Path to the PNG icon to overlay
    :param position_ratio: Tuple (x_ratio, y_ratio), each from 0 to 1, for proportional position
    :param scale_ratio: Ratio (0 to 1) of the icon's width to the QR image's width
    :return: New PIL Image with the icon overlaid
    """
    # Load and resize the icon
    icon = Image.open(icon_path).convert("RGBA")
    qr_width, qr_height = qr_image.size
    icon_size = int(min(qr_width, qr_height) * scale_ratio)
    icon = icon.resize((icon_size, icon_size), Image.LANCZOS)

    # Calculate placement position
    x = int(qr_width * position_ratio[0] - icon_size / 2)
    y = int(qr_height * position_ratio[1] - icon_size / 2)

    # Create a new image and paste everything
    combined = qr_image.copy()
    combined.paste(icon, (x, y), icon)  # use icon as mask to retain transparency

    return combined