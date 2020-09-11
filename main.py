import os
import requests
from dotenv import load_dotenv
import argparse


def shorten_link(token, link):
    url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {'Authorization': "Bearer " + token}
    payload = {"long_url": link}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["link"]


def count_clicks(token, link):
    url = "https://api-ssl.bitly.com/v4/bitlinks/%s/clicks/summary" % link
    headers = {'Authorization': "Bearer " + token}
    response = requests.get(url, headers=headers)
    return response.json()["total_clicks"]


def main():
    load_dotenv()
    BITLY_TOKEN = os.getenv("BITLY_TOKEN")
    parser = argparse.ArgumentParser(description='Программа сокращает ссылки '
                                                 'и выдает статистику '
                                                 'переходов по ним')
    parser.add_argument('link', help='Ссылка для сокращения '
                                     'или проверки статистики переходов')
    args = parser.parse_args()
    url = args.link
    if url.startswith(("https://bit.ly", "bit.ly")):
        try:
            print('Количество переходов по ссылке:',
                  count_clicks(BITLY_TOKEN, url.replace("https://", "")))
        except requests.exceptions.HTTPError:
            print("Ошибка")
    else:
        try:
            print('Битлинк', shorten_link(BITLY_TOKEN, url))
        except requests.exceptions.HTTPError:
            print("Ошибка")


if __name__ == '__main__':
    main()
