import pytesseract
from PIL import Image

# путь к исполняемому файлу.
pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR/tesseract.exe"

def teseract_recognition(path_img):
    return pytesseract.image_to_string(Image.open(path_img), lang='rus+eng', config=r'--oem 3 --psm 6')