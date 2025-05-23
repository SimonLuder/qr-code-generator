from pyqrcode.generator import QrCodeGenerator

if __name__ == "__main__":

    QrCodeGenerator(data="This is a test", 
                    outfile="output/test.png", 
                    inner_eye_color=(100, 23, 100), 
                    outer_eye_style="Rounded"
                    ).generate()