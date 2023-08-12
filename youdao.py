import re

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua.random,
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }


def get_exam_type(word):
    """从有道获取单词所属的词本范围"""
    params = {
        'word': word,
        'lang': 'en',
    }

    try:

        response = requests.get(f'https://dict.youdao.com/result', params=params, headers=headers)

        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        exam_type_tmp = soup.select('.exam_type>.exam_type-value')

        exam_types = [exam_type.text for exam_type in exam_type_tmp]

        return ', '.join(exam_types)
    except Exception as e:
        print('YouDao Error: ', e)
        return ''


if __name__ == '__main__':
    get_exam_type('holiday')