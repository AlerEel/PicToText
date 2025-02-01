import unittest
from unittest.mock import patch, mock_open, MagicMock
from PIL import Image
import io

# Импортируем тестируемый модуль 
from PicToTextStreamlit import load_image  

class TestApp(unittest.TestCase):
    def setUp(self):
        # Создаем тестовое изображение
        self.test_image = Image.new('RGB', (100, 100), color='white')
        self.image_bytes = io.BytesIO()
        self.test_image.save(self.image_bytes, format='PNG')
        self.image_bytes.seek(0)

    @patch('streamlit.file_uploader')
    def test_load_image_with_file(self, mock_file_uploader):
        # Мокируем st.file_uploader, чтобы он возвращал тестовое изображение
        mock_uploaded_file = MagicMock()
        mock_uploaded_file.getvalue.return_value = self.image_bytes.getvalue()
        mock_file_uploader.return_value = mock_uploaded_file

        # Вызываем функцию load_image
        result = load_image()

        # Проверяем, что результат является объектом PIL.Image
        self.assertIsInstance(result, Image.Image)

    @patch('streamlit.file_uploader')
    def test_load_image_without_file(self, mock_file_uploader):
        # Мокируем st.file_uploader, чтобы он возвращал None
        mock_file_uploader.return_value = None

        # Вызываем функцию load_image
        result = load_image()

        # Проверяем, что результат равен None
        self.assertIsNone(result)

    @patch('pytesseract.image_to_string')
    def test_text_recognition(self, mock_image_to_string):
        # Мокируем pytesseract.image_to_string, чтобы он возвращал тестовый текст
        mock_image_to_string.return_value = "Test text"

        from app import img_to_text  # Предполагается, что функция распознавания называется img_to_text
        result = img_to_text(self.test_image)

        # Проверяем, что результат содержит ожидаемый текст
        self.assertEqual(result, "Test text")

if __name__ == '__main__':
    unittest.main()