import os


def get_words_from_txt():
    # 从文件中读取单词
    words = set()
    with open('Collect/words.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            words.add(line.strip().lower())

    return words