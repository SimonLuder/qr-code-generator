from pyqrcode.generator import QrCodeGenerator

if __name__ == "__main__":

    # Example 1 basic QR code generation
    QrCodeGenerator(data="AddYourUrlHere", 
                    outfile="output/example1.png", 
                    ).generate()

    # Example 2 with styling options
    qr = QrCodeGenerator(
        data="https://github.com/SimonLuder",                                              
        outfile="output/example2.png",
        logo="images/profile_img.png",
        sub_logo="images/github-mark.png",
        front_image=None,
        bar_style="Rounded",
        front_color=(255, 255, 255),
        back_color=(1, 1, 1),
        outer_eye_color=(210, 186, 132),
        outer_eye_style="Rounded",
        inner_eye_color=(255, 226, 160),
        inner_eye_style="Rounded",
        bottom_text="github.com/SimonLuder/qr-code-generator",
        bottom_text_color=(255, 255, 255),
        bottom_text_size=42,
        bottom_text_font="default",
        radius_ratio=0.1,
        box_size=30, 
        ).generate()
