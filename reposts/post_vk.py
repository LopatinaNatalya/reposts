import os, requests
from dotenv import load_dotenv


def get_vk(method, payload):
    url = 'https://api.vk.com/method/{}?v=5.95'.format(method)

    response = requests.get(url, params=payload)
    response.raise_for_status()

    if 'error' in response.text:
        raise requests.exceptions.HTTPError()

    return response.json().get('response')


def get_server_address_to_upload_album_photos(access_token, album_id, group_id):
    """Получение url для загрузки фотографии в альбом."""
    method = 'photos.getUploadServer'
    payload = {
        'album_id':album_id,
        'group_id':group_id,
        'access_token':access_token,
    }

    response = get_vk(method, payload)
    return None if response is None else response['upload_url']


def upload_photo(upload_url, filepath, caption):
    """Загрузка фотографии."""
    hash = None
    server = None
    photos_list = None

    with open(filepath, 'rb') as photo_file:
        files = {
            'photo': photo_file,
            'Content-Type': 'multipart/form-data.',
            'caption': caption
                }

        response = requests.post(upload_url, files=files)
        response.raise_for_status()

        if 'error' in response.text:
            raise requests.exceptions.HTTPError()

        if response is not None:
            hash = response.json()['hash']
            server = response.json()['server']
            photos_list = response.json()['photos_list']

    return hash, server, photos_list


def save_album_photo(access_token, album_id, group_id, photos_list, hash, server, caption):
    """Cохранение фотографии в альбом."""
    method = 'photos.save'
    payload = {
        'album_id':album_id,
        'group_id':group_id,
        'photos_list':photos_list,
        'hash':hash,
        'server':server,
        'caption':caption,
        'access_token':access_token,
    }

    response = get_vk(method, payload)
    return None if response is None else 'photo{}_{}'.format(str(response[0]['owner_id']), str(response[0]['id']))


def post_on_wall(access_token, message, group_id, attachments=''):
    """Выкладывает пост на стену.
       Если attachments не указан, выкладывается только сообщение.
       Если attachments указан, выкладывается фотография.
    """
    method = 'wall.post'
    payload = {
        'owner_id':'-' + group_id,
        'from_group': '1',
        'message':message,
        'attachments':attachments,
        'access_token':access_token,
    }

    get_vk(method, payload)


def post_image(access_token, group_id, album_id, filepath, caption):
    upload_url = get_server_address_to_upload_album_photos(access_token, album_id, group_id)
    if upload_url is None:
        return

    hash, server, photos_list = upload_photo(upload_url, filepath, caption)
    if hash is None or server is None or photos_list is None:
        return

    attachments = save_album_photo(access_token, album_id, group_id, photos_list, hash, server, caption)
    if attachments is None:
        return

    title = ''
    post_on_wall(access_token, title, group_id, attachments)


def post_vkontakte(image_filepath=None, text_filepath=None):
    access_token = os.getenv("VK_ACCESS_TOKEN")
    group_id = os.getenv("VK_GROUP_ID")
    album_id = os.getenv("VK_ALBUM_ID")
    text = ''

    if image_filepath is None and text_filepath is None:
        raise ValueError('А что постим? Укажите путь до текста или картинки.')

    if text_filepath is not None:
        with open(text_filepath, 'r', encoding="utf-8") as text_file:
            text = text_file.read()
        if image_filepath is None:
            post_on_wall(access_token, text, group_id)

    if image_filepath is not None:
        post_image(access_token, group_id, album_id, image_filepath, text)


def main():
    load_dotenv()
    image_filepath = r'D:\files\пример для картинки.png'
    text_filepath = r'D:\files\пример для теста.txt'
    try:
        post_vkontakte(image_filepath, text_filepath)
    except ValueError as no_files_for_post:
        print(no_files_for_post)

    except requests.exceptions.HTTPError:
        print('Ошибочный запрос')

    except requests.exceptions.ConnectionError:
        print('Отсутствует сетевое соединение')

    except requests.exceptions.ConnectTimeout:
        print('Превышено время ожидания')


# raise requests.exceptions.HTTPError()
if __name__ == "__main__":
  main()
