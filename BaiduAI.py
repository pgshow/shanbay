# encoding:utf-8
from keys import account
from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '26474578'
API_KEY = 'CO4FiK5sjbZKC3gjgaV7aNiz'
SECRET_KEY = account.SECRET_KEY

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def pic2word(image):
    # 如果有可选参数
    options = {
        "language_type": "CHN_ENG",
        "detect_direction": "true",
        "detect_language": "true",
        "probability": "true"
    }

    # res_url = client.basicGeneralUrl('https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png', options)'
    return client.basicGeneral(image, options)


if __name__ == '__main__':
    word = pic2word('')