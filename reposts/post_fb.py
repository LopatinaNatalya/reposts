import os, requests
from dotenv import load_dotenv


def post_message_on_wall(access_token, message, group_id):
    """Выкладывает пост на стену"""
    payload = {
        'message':message,
        'access_token':access_token,
    }

    url = 'https://graph.facebook.com/v3.3/{}/feed'.format(group_id)
    requests.post(url, params=payload)


def post_photo_on_wall(filepath, caption, access_token, group_id):
    """Выкладываем фотография на стену группы"""
    with open(filepath, 'rb') as photo_file:
        files = {
            'file': photo_file,
            'Content-Type': 'multipart/form-data.',
            }
        payload = {
            'caption': caption,
            'access_token': access_token,
        }

        url = 'https://graph.facebook.com/v3.3/{}/photos'.format(group_id)
        requests.post(url, files=files, params=payload)


def post_facebook(image_filepath=None, text_filepath=None):
    load_dotenv()
    access_token = os.getenv("FB_ACCESS_TOKEN")
    group_id = str(os.getenv("FB_GROUP_ID"))
    text = ''

    if image_filepath is None and text_filepath is None:
        return

    if text_filepath is not None:
        with open(text_filepath, 'r', encoding="utf-8") as text_file:
            text = text_file.read()
        if image_filepath is None:
            post_message_on_wall(access_token, text, group_id)

    if image_filepath is not None:
         post_photo_on_wall(image_filepath, text, access_token, group_id)


def main():
    image_filepath = r'D:\files\пример для картинки.png'
    text_filepath = r'D:\files\пример для теста.txt'

    post_facebook(image_filepath, text_filepath)


if __name__ == "__main__":
  main()
