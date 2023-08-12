import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,ja;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'dicthe=CzrC4hYTC4ROdz4bDbC48XNB4uBLz46rPB44pPz4Fc7C4p7Mx4dOFA47W7y4Jo5C4%2Ftaunt%2Funison%2Ffearsome%2Fspotter%2Fsandals',
    'DNT': '1',
    'Referer': 'http://dict.cn/unison',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
}

response = requests.get('http://dict.cn/taunt', headers=headers, verify=False)

print(response.text)
print(response.status_code)