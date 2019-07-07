import os, telegram
from dotenv import load_dotenv


def post_message(bot, chat_id, message):
  return bot.send_message(chat_id, message)


def post_image(bot, chat_id, image_filepath, caption):
  bot.send_photo(chat_id=chat_id, photo=open(image_filepath, 'rb'), caption=caption)


def post_telegram(image_filepath=None, text_filepath=None):
    load_dotenv()
    access_token = os.getenv("TG_ACCESS_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")
    bot = telegram.Bot(access_token)
    text = ''

    if image_filepath is None and text_filepath is None:
        return

    if text_filepath is not None:
        with open(text_filepath, 'r', encoding="utf-8") as text_file:
            text = text_file.read()
        if image_filepath is None:
            post_message(bot, chat_id, text)

    if image_filepath is not None:
        post_image(bot, chat_id, image_filepath, text)


def main():
    image_filepath = r'D:\files\пример для картинки.png'
    text_filepath = r'D:\files\пример для теста.txt'

    post_telegram(image_filepath, text_filepath=text_filepath)


if __name__ == "__main__":
  main()
