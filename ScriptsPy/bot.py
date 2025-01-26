import telebot
from moviepy.editor import AudioFileClip
import speech_recognition as sr
import pytesseract
import easyocr
from PIL import Image
import io

TOKEN = '7103546657:AAGnxgN-0tNCwZpBLkBDaVH7BchzFRBqFqk'
bot = telebot.TeleBot(token=TOKEN)

# путь к исполняемому файлу.
pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR/tesseract.exe"

# Функция для сканирования изображения с помощью tesseract
def teseract_recognition(path_img):
    return easyocr.Reader(["ru"]).readtext(path_img, detail=0, paragraph=True, text_threshold=0.8)


# приветственное сообщение
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 f'Привет, {message.chat.first_name}! Я бот, который умеет конвертировать голосовые сообщения в текст.\nЧтобы начать, просто перешли мне голосовое сообщение.')


# вывод возможностей бота после нажатия на кнопку "старт"
@bot.message_handler(commands=['help'])
def bot_capabilities(message):
    bot.reply_to(message, 'Я могу конвертировать голосовые сообщения и изображения в текст.\nПросто перешли мне голосовое сообщение, которое необходимо конвертировать.')

@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, "Отправьте картинку или аудио.")

# функция, которая будет вызываться при получении голосового сообщения
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    # проверка на наличие пересланного сообщения
    if message:
        bot.reply_to(message, 'Подождите немного, я обрабатываю голосовое сообщение :)')
        file_id = message.voice.file_id
        file = bot.get_file(file_id)
        file_path = file.file_path

        # загрузка голосовой записи с серверов Telegram
        downloaded_file = bot.download_file(file_path)
        with open('../data/audio.ogg', 'wb') as new_file:
            new_file.write(downloaded_file)

        # преобразование голосовой записи в текст
        audio = AudioFileClip('../data/audio.ogg')
        audio.write_audiofile('../data/audio.wav')
        recognizer = sr.Recognizer()
        with sr.AudioFile('../data/audio.wav') as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='ru-RU')

        # ответ на голосовое сообщение текстом
        bot.reply_to(message, text)
    else:
        bot.reply_to(message, 'Пересланных голосовых сообщений не найдено')

@bot.message_handler(content_types=['audio'])
def voice_processing(message):
    # проверка на наличие пересланного сообщения
    if message:
        bot.reply_to(message, 'Подождите немного, я обрабатываю сообщение :)')

        file_id = message.audio.file_id
        file = bot.get_file(file_id)
        file_path = file.file_path

        # загрузка голосовой записи с серверов Telegram
        downloaded_file = bot.download_file(file_path)
        with open('../data/audio.mp3', 'wb') as new_file:
            new_file.write(downloaded_file)

        # преобразование голосовой записи в текст
        audio = AudioFileClip('../data/audio.mp3')
        audio.write_audiofile('../data/audio.wav')
        recognizer = sr.Recognizer()
        with sr.AudioFile('../data/audio.wav') as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='ru-RU')

        # ответ на голосовое сообщение текстом
        bot.reply_to(message, text)
    else:
        bot.reply_to(message, 'Пересланных голосовых сообщений не найдено')

@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    img = Image.open(io.BytesIO(downloaded_file))

    # ответ на голосовое сообщение текстом
    bot.reply_to(message, pytesseract.image_to_string(img, lang='rus+eng', config=r'--oem 3 --psm 6'))



if __name__ == '__main__':
    bot.polling(none_stop=True)