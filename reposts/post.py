import argparse, post_fb, post_tg, post_vk


def posts(social_network, image_filepath, text_filepath):
    if 'vk' in social_network:
        post_vk.post_vkontakte(image_filepath, text_filepath)

    if 'tg' in social_network:
        post_tg.post_telegram(image_filepath, text_filepath)

    if 'fb' in social_network:
        post_fb.post_facebook(image_filepath, text_filepath)


def main():
    parser = argparse.ArgumentParser(
       description='''Размещаем пост в Telegram-канале и группах Вконтакте и Facebook'''
    )
    parser.add_argument('--social_network',
            help='''Укажите в какую социальную сеть необходимо опубликовать пост:
                            vk - будет опубликован в группе Вконтакте,
                            tg - будет опубликован в Telegram-канале,
                            fb - будет опубликован в группе Facebook,
                            если ничего не указывать - пост будет опубликован во все социальные сети''')
    parser.add_argument('--image_filepath',
            help='''Укажите путь до файла с картинкой или фотогрвфией''')
    parser.add_argument('--text_filepath',
            help='''Укажите путь до файла с текстом''')

    args = parser.parse_args()
    social_network = args.social_network if args.social_network else 'vk,fb,tg'
    image_filepath = args.image_filepath
    text_filepath = args.text_filepath

    if image_filepath is None and text_filepath is None:
        print ('А что постим? Укажите путь до текста или картинки.')
        return

    posts(social_network, image_filepath, text_filepath)


if __name__ == "__main__":
  main()
