import re
import time
import threading
import pyperclip
import pyautogui
import threading

import BaiduAI
import mouseAct
import textshot
import program
from shanbay import Shanbay
from loguru import logger
from queue import Queue
from pynput import mouse


class Bot(object):
    def __init__(self):
        self.CMDs = Queue(maxsize=0)
        self.windowSize = pyautogui.size()
        self.shanbay_cls = Shanbay()
        self.potplayer_title = None

        # 鼠键行为变量
        self.copyWordTime = 0  # 打开单词复制面板的时间
        self.pressTime = 0  # 鼠标中键按下的时间

    def control(self):
        while True:
            cmd = self.CMDs.get()
            if cmd['act'] == 'snapshot':
                # 暂停播放
                # pyautogui.press('space')
                self.potplayer_title = pyautogui.getActiveWindowTitle

                # 截图识字然后在扇贝搜索
                pic_bin = textshot.snap()
                if not pic_bin:
                    continue

                try:
                    result = BaiduAI.pic2word(pic_bin)  # ocr 识别结果
                    if 'words_result' not in result or result['words_result_num'] == 0:
                        logger.error(result)

                    else:

                        words = result['words_result'][0]['words']

                        words_trimmed = re.sub(r'[^a-zA-Z -]', '', words)

                        logger.debug(f'Ocr 识别到单词: {words_trimmed}')

                        self.shanbay_cls.show()

                        self.shanbay_cls.search_word(words_trimmed)
                except RuntimeError as e:
                    logger.error(f'AI识别文字发生错误: {e}')

            elif cmd['act'] == 'byText':
                # 从剪切板搜索单词
                pass

    def monitor_hotkeys(self):
        with mouse.Listener(on_click=self.on_mouse_middle_click) as listener:
            listener.join()

    def pool(self):
        t1 = threading.Thread(target=self.control, name='Control_Thread')
        t2 = threading.Thread(target=self.monitor_hotkeys, name='Monitor_Thread')
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def on_mouse_middle_click(self, x, y, button, pressed):
        """
        PotPlayer 窗口单击鼠标中键，打开截图识别英语单词的功能
        PotPlayer 字幕上双击鼠标中键，自动判断是否字幕，然后复制到剪切板并查询
        """
        if button.name != 'middle' or not program.is_the_app():
            # 必须是鼠标中键在 PotPlayer 上的行为
            return

        if pressed:
            self.pressTime = time.time()

            if mouseAct.single_double_click(x, y) == 1:
                act = {
                    'x': x,
                    'y': y,
                    'act': 'snapshot',
                }
                self.CMDs.put_nowait(act)
                # return True


if __name__ == '__main__':
    bot = Bot()
    bot.pool()
