import re

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,ja;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'http://dict.cn/unison',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
}


def get_exam_range(word):
    """从海词获取单词所属的词本范围"""
    try:

        response = requests.get(f'http://dict.cn/{word}', headers=headers)

        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        if soup.select_one('span.level-title') is None:
            print('HaiCi has no level-title for this word')
            return '0'

        exam_range_tmp = soup.select_one('span.level-title').get('level')

        exam_range = re.search(r'(\d{4,5})', exam_range_tmp).group(1)

        return exam_range
    except Exception as e:
        print('HaiCi Error: ', e)
        return ''


if __name__ == '__main__':
    result = get_exam_range('dissertations')
    print(result)