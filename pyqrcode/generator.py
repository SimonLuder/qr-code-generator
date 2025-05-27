import os
import shutil
from PIL import Image, ImageDraw
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, HorizontalBarsDrawer, VerticalBarsDrawer, SquareModuleDrawer, GappedSquareModuleDrawer
from  qrcode.image.styles.colormasks import SolidFillColorMask, ImageColorMask

from pyqrcode.overlays import add_overlay_icon
from pyqrcode.text import add_text_to_image 


class QrCodeGenerator:
    def __init__(self, 
                 data: str, 
                 outfile: str, 
                 logo: str=None, 
                 sub_logo: str=None, 
                 front_image: str=None, 
                 bar_style: str="Square",
                 front_color: tuple[int, int, int]=(0, 0, 0), 
                 back_color: tuple[int, int, int]=(255, 255, 255),
                 outer_eye_style: str=None, 
                 outer_eye_color: tuple[int, int, int]=None,
                 inner_eye_color: tuple[int, int, int]=None, 
                 inner_eye_style: str=None, 
                 bottom_text: str=None, 
                 bottom_text_color: tuple[int, int, int]=(0, 0, 0), 
                 bottom_text_size: int=42, 
                 bottom_text_font: str=None,
                 box_size: int=10, 
                 radius_ratio: float=0.5, 
            ):
        
        self.data = data
        self.outfile = outfile
        self.logo = logo
        self.sub_logo = sub_logo
        self.front_image = front_image
        self.front_color = front_color
        self.back_color = back_color
        self.bar_style = bar_style
        self.inner_eye_color = inner_eye_color
        self.inner_eye_style = inner_eye_style
        self.outer_eye_color = outer_eye_color
        self.outer_eye_style = outer_eye_style
        self.radius_ratio = radius_ratio
        self.bottom_text = bottom_text
        self.bottom_text_color = bottom_text_color
        self.bottom_text_size = bottom_text_size
        self.bottom_text_font = bottom_text_font
        self.box_size = box_size


    def get_drawer(self, style):
        drawers = {
            "Square": SquareModuleDrawer,
            "GappedSquare": GappedSquareModuleDrawer,
            "HorizontalBars": HorizontalBarsDrawer,
            "VerticalBars": VerticalBarsDrawer,
            "Rounded": RoundedModuleDrawer,
            "Circle": CircleModuleDrawer,
        }
        return drawers[style]()
    

    def crop_and_round_image(self, input_path, output_path="temp/temp.png"):
        image = Image.open(input_path).convert("RGBA")
        width, height = image.size
        min_side = min(width, height)
        left = (width - min_side) // 2
        top = (height - min_side) // 2
        image = image.crop((left, top, left + min_side, top + min_side))

        radius = int(min_side * self.radius_ratio)
        mask = Image.new("L", (min_side, min_side), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, min_side, min_side], radius=radius, fill=255)

        rounded = Image.new("RGBA", (min_side, min_side), (0, 0, 0, 0))
        rounded.paste(image, (0, 0), mask)
        rounded.save(output_path, format="PNG")
        return output_path
        

    def apply_outer_eye_style(self, qr_img):

        # Style the outer part of the eye
        if self.outer_eye_color is not None or self.outer_eye_style is not None:

            kwargs = self.style_kwargs

            # Custom eye color if given
            if self.outer_eye_color is not None:
                kwargs["color_mask"] = SolidFillColorMask(front_color=self.outer_eye_color, 
                                                      back_color=self.back_color)
                
            # Custom eye style if given
            if self.outer_eye_style is None:
                self.outer_eye_style = self.bar_style
            kwargs["eye_drawer"] = self.get_drawer(self.outer_eye_style)
        
            qr_outer_eyes_img = self.qr.make_image(**kwargs)
            outer_eye_mask = self.create_outer_eye_mask(qr_img)   
            qr_outer_eyes_img = qr_outer_eyes_img.convert("RGBA")
            qr_img = Image.composite(qr_outer_eyes_img, qr_img, outer_eye_mask)
        
        return qr_img
    
    
    def apply_inner_eye_style(self, qr_img):

        # Style the inner part of the eye
        if self.inner_eye_color is not None or self.inner_eye_style is not None:

            kwargs = self.style_kwargs

            # Custom eye color if given
            if self.inner_eye_color is not None:
                kwargs["color_mask"] = SolidFillColorMask(front_color=self.inner_eye_color, 
                                                          back_color=self.back_color)

            # Custom eye style if given
            if self.inner_eye_style is None:
                self.inner_eye_style = self.bar_style
            kwargs["eye_drawer"] = self.get_drawer(self.inner_eye_style)
        
            qr_inner_eyes_img = self.qr.make_image(**kwargs)
            inner_eye_mask = self.create_inner_eye_mask(qr_img)
            qr_inner_eyes_img = qr_inner_eyes_img.convert("RGBA")
            qr_img = Image.composite(qr_inner_eyes_img, qr_img, inner_eye_mask)

        return qr_img
    
    
    def create_inner_eye_mask(self, img: Image) -> Image:
        """
        Generate a mask highlighting the inner 3x3 modules of the QR code's position markers.

        Args:
            img (PIL.Image): The input QR code image (assumed to be square).

        Returns:
            PIL.Image: A grayscale mask image with the inner eye regions in white (255) and the rest in black (0).
        """
        img_size = img.size[0]
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)

        # Inner eyes are 3x3 modules, starting at (3, 3) offset
        offset = 6 * self.box_size
        size = 3 * self.box_size

        draw.rectangle((offset, offset, offset + size, offset + size), fill=255)  # top-left
        draw.rectangle((img_size - offset - size, offset, img_size - offset, offset + size), fill=255)  # top-right
        draw.rectangle((offset, img_size - offset - size, offset + size, img_size - offset), fill=255)  # bottom-left

        return mask


    def create_outer_eye_mask(self, img: Image) -> Image:
        """
        Generate a mask highlighting the outer 7x7 modules of the QR code's position markers.

        Args:
            img (PIL.Image): The input QR code image (assumed to be square).

        Returns:
            PIL.Image: A grayscale mask image with the outer eye regions in white (255) and the rest in black (0).
        """
        img_size = img.size[0]
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)

        # Outer eyes are 7x7 modules, starting at (0, 0)
        outer_size = 7 * self.box_size
        inner_offset = 4 * self.box_size
        inner_size = 3 * self.box_size

        # Outer rectangles
        draw.rectangle((inner_offset, inner_offset, inner_offset + outer_size, inner_offset + outer_size), fill=255)  # top-left
        draw.rectangle((img_size - (inner_offset + outer_size), inner_offset, img_size - inner_offset, inner_offset + outer_size), fill=255)  # top-right
        draw.rectangle((inner_offset, img_size - (inner_offset + outer_size), (inner_offset + outer_size), img_size-inner_offset), fill=255)  # bottom-left

        return mask
    

    def generate(self):

        os.makedirs("temp/", exist_ok=True)

        # Crop and round the logo image
        if self.logo:
            styled_logo = self.crop_and_round_image(self.logo)
        else:
            styled_logo = None

        # Generate qr-code
        self.qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=self.box_size)

        # Add message to the qr-code
        self.qr.add_data(self.data)

        self.style_kwargs = {
            "image_factory": StyledPilImage,
        }

        # Use background image if exists, else color
        if self.front_image is not None:
            self.style_kwargs["color_mask"] = ImageColorMask(color_mask_path=self.front_image, 
                                                             back_color=self.back_color)
        else:
            self.style_kwargs["color_mask"]  = SolidFillColorMask(front_color=self.front_color, 
                                                                  back_color=self.back_color)

        # Select bar draw style
        self.style_kwargs["module_drawer"] = self.get_drawer(self.bar_style)

        # Use logo
        if styled_logo:
            self.style_kwargs["embeded_image_path"] = styled_logo

        qr_img = self.qr.make_image(**self.style_kwargs)
        qr_img = qr_img.convert("RGBA")

        qr_img = self.apply_outer_eye_style(qr_img)

        qr_img = self.apply_inner_eye_style(qr_img)

        # Overlay additional icon (optional)
        if self.sub_logo is not None:
            qr_img = add_overlay_icon(qr_img, icon_path=self.sub_logo, 
                                      position_ratio=(0.5, 0.65), scale_ratio=0.12)
            
        # Add text on bottom (optional)
        if self.bottom_text is not None:
            qr_img = add_text_to_image(qr_img, self.bottom_text, 0.5, 0.95, self.bottom_text_color, 
                                       self.bottom_text_font, self.bottom_text_size)

        # Save qr-code to oufile path
        qr_img.save(self.outfile)

        # Remove temporary folder
        shutil.rmtree("temp/")
