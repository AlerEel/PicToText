import io
import streamlit as st
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\User\PycharmProjects\python_Tesseract\Tesseract-OCR\tesseract.exe"
def load_image():
    """Создание формы для загрузки изображения"""
    # Форма для загрузки изображения средствами Streamlit
    uploaded_file = st.file_uploader(
        label='Выберите изображение для распознавания')
    if uploaded_file is not None:
        # Получение загруженного изображения
        image_data = uploaded_file.getvalue()
        # Показ загруженного изображения на Web-странице средствами Streamlit
        st.image(image_data)
        # Возврат изображения в формате PIL
        return Image.open(io.BytesIO(image_data))
    else:
        return None

result = None
# Выводим заголовок страницы средствами Streamlit
st.title('Классификация изображений')
# Вызываем функцию создания формы загрузки изображения
img = load_image()
if img:
    # Вызываем функцию распознавания изображения
    result = st.button('Распознать изображение')

if result:
    # Распознавание изображения
    preds = pytesseract.image_to_string(img, lang='rus+eng', config=r'--oem 3 --psm 6')
    # Выводим заголовок результатов распознавания жирным шрифтом
    # используя форматирование Markdown
    st.write('**Результаты распознавания:**')
    # Выводим результаты распознавания
    st.write(preds)
