import time
import pyautogui
import pyperclip
from loguru import logger


def is_the_apps():
    """判断是否是需要截屏的目标程序"""
    active_window = pyautogui.getActiveWindow()
    if active_window:
        # print(active_window.title)
        if active_window.title.endswith('PotPlayer'):
            logger.debug(f'在 PotPlayer 播放器上截图')
            return True
        elif active_window.title.startswith('课程'):
            logger.debug(f'在 51Talk 课件上截图')
            return True
        elif ' - YouTube 和另外 ' in active_window.title:
            logger.debug(f'在 Youtube 上截图')
            return True
        elif ' - 喜马拉雅' in active_window.title:
            logger.debug(f'在 Ximalaya 上截图')
            return True


def is_chrome():
    active_window = pyautogui.getActiveWindow()
    if not active_window.title.endswith('扇贝，知道你在改变 - Google Chrome'):
        return False


def player_get_word():
    """从字幕获取单词"""
    word = None
    for i in range(9):
        time.sleep(0.3)
        word = pyperclip.paste()
        if word:
            logger.success(f'复制单词 {word}')
            return word

    if not word:
        logger.error(f'复制单词失败')
        return


def pause_potplayer():
    """播放暂停"""


if __name__ == '__main__':
    windowSize = pyautogui.size()
    player_get_word(windowSize)