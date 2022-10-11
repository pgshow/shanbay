import time

import pyperclip
import pyautogui
import threading

import BaiduAI
import mouseAct
import textshot
import program
from shanbay import Shanbay
from pynput import mouse
from loguru import logger

pyautogui.PAUSE = 0.005

pressTime = 0
windowSize = pyautogui.size()
# shanbay_cls = Shanbay()

copyWordTime = 0  # 打开单词复制面板的时间


def on_mouse_right_click(x, y, button, pressed):
    """
    PotPlayer播放器下方点击鼠标右键
    直接复制字幕
    """
    global copyWordTime

    if button.name == 'right':
        # 鼠标右键出菜单
        if not program.is_the_apps():
            return

        if not pressed:
            time.sleep(2)

            for i in range(3):
                time.sleep(0.4)
                # 如果出现复制菜单，记下出现的时间
                pos = pyautogui.locateOnScreen('./img/potplayer-clipboard.png', region=(x+35, y+150, windowSize.width, windowSize.height), grayscale=True)  # 出现复制菜单

                if pos:
                    im = pyautogui.screenshot(region=(x + 35, y + 150, windowSize.width, windowSize.height))
                    im.save('test.jpg')
                    pyperclip.copy('')  # 清空剪切板
                    copyWordTime = time.time()
                    break

    elif button.name == 'left':
        # 鼠标左键选择复制
        delay = time.time() - copyWordTime

        if delay > 8:
            # 短时间内才能算单词搜索
            return

        copyWordTime = 0

        # 短时间内单机鼠标左键视为复制单词
        if not program.is_the_apps():
            return

        if pressed:
            word = program.player_get_word()
            if not word:
                return
            shanbay_cls.search_word(word)


def on_mouse_middle_click(x, y, button, pressed):
    """
    PotPlayer 中不能复制的字幕，只能用截图识字的方式
    """
    if button.name != 'middle':
        # 鼠标中键
        return

    global pressTime
    if pressed:
        pressTime = time.time()

        if not program.is_the_apps():
            return

        if mouseAct.single_double_click(x, y):
            # 截图识字然后在扇贝搜索
            pic_bin = textshot.snap()
            BaiduAI.pic2word(pic_bin)




if __name__ == '__main__':
    # listener = mouse.Listener(on_click=on_mouse_middle_click,suppress=True)
    listener1 = mouse.Listener(on_click=on_mouse_middle_click)
    listener1.start()

    listener2 = mouse.Listener(on_click=on_mouse_right_click)
    listener2.start()

    while True:
        time.sleep(1)

