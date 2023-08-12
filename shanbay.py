import sys
import time
import pyautogui
import read_dict
import youdao
import haici
from keys import account
from loguru import logger
from safe_driver import SafeDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

USER = account.USER
PASSWORD = account.PASSWORD


class Shanbay:
    def __init__(self):
        self.browser_title1 = '扇贝，知道你在改变'
        self.browser_title2 = '有道词典识别'
        self.browser_title3 = '海词词典识别'
        self.shanbay_window = None
        self.youdao_window = None
        self.haici_window = None
        self.words = read_dict.get_words_from_txt()
        self.driver = SafeDriver().driver
        self.login(self.driver)

    def search_word(self, word):
        """从扇贝搜索单词"""
        logger.info(f'搜索单词 {word}')

        driver = self.driver
        try:
            # 切换到扇贝窗口
            driver.switch_to.window(self.shanbay_window)
            driver.get('https://web.shanbay.com/web/main/index')
            driver.find_element(By.CSS_SELECTOR, 'div.searchContainer > input').send_keys(word)
            time.sleep(1)
            # await asyncio.sleep(1)
            driver.find_element(By.CSS_SELECTOR, 'div.searchContainer .submit').click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.head-word')))
            time.sleep(1)

            # driver.maximize_window()
            if word.lower() in self.words:
                # 查看单词是否属于扇贝8000词雅思词
                logger.success(f'单词 {word} 属于8000雅思词')
                driver.execute_script("word = document.getElementsByClassName('head-word')[0].innerText; document.getElementsByClassName('head-word')[0].innerHTML = word + ' <span style=\"color:grey\">- in 8000</span>'")
                time.sleep(5)
            else:
                # 查看单词在考试中的难度范围
                exam_type = youdao.get_exam_type(word)
                exam_range = haici.get_exam_range(word)
                if exam_type:
                    logger.success(f'单词 {word} 属于 {exam_type}, 单词表范围 {exam_range}')
                    driver.execute_script("word = document.getElementsByClassName('head-word')[0].innerText; document.getElementsByClassName('head-word')[0].innerHTML = word + '<p style=\"color:grey; font-size:10px;\">- " + exam_type + "</p><p style=\"color:grey; font-size:10px;\">- 属 " + exam_range + "</p>'")
                    time.sleep(5)

            # # 切换到有道窗口
            # driver.switch_to.window(self.youdao_window)
            # driver.get(f'https://dict.youdao.com/result?word={word}&lang=en')
            # time.sleep(3)
            # driver.execute_script('document.title="有道词典识别"')

            # time.sleep(1)
            #
            # # 切换到海词窗口
            # driver.switch_to.window(self.haici_window)
            # driver.get(f'http://dict.cn/{word}')
            # time.sleep(3)
            # driver.execute_script('document.title="海词词典识别"')
        except Exception as e:
            logger.error(f'搜索发生错误: {e}')

    def login(self, driver):
        self.close_previous()

        driver.get('https://web.shanbay.com/web/account/login/')

        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//h3[text()="欢迎来到扇贝"]')))
        except:
            logger.error('登录 扇贝出错')
            return

        driver.find_element(By.ID, 'input-account').send_keys(USER)
        time.sleep(1)
        driver.find_element(By.ID, 'input-password').send_keys(PASSWORD)
        time.sleep(1)
        driver.find_element(By.ID, 'button-login').click()
        time.sleep(2)

        try:
            # 滑动解锁
            slider = WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.btn_slide')))

            action = ActionChains(driver)

            action.click_and_hold(slider).perform()  # 鼠标左键按住不放

            action.move_by_offset(258, 0)
            action.pause(0.5).release().perform()

            WebDriverWait(driver, 45).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.btn_slide')))

            time.sleep(1)

            driver.find_element(By.ID, 'button-login').click()

            WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.searchContainer')))

            logger.success('扇贝登录成功')

            self.shanbay_window = self.driver.window_handles[0]  # 获取扇贝窗口句柄

            # # 有道词典
            #
            # self.driver.execute_script('window.open("")')  # 打开一个新的空白窗口
            #
            # self.youdao_window = self.driver.window_handles[-1]  # 获取有道窗口句柄
            #
            # self.driver.switch_to.window(self.youdao_window)  # 切换到有道窗口
            #
            # time.sleep(1)
            #
            # # Change youdao title
            # self.driver.execute_script("document.title = '有道词典识别'")

            # # 海词词典
            #
            # self.driver.execute_script('window.open("")')  # 打开一个新的空白窗口
            #
            # self.haici_window = self.driver.window_handles[-1]  # 获取海词窗口句柄
            #
            # self.driver.switch_to.window(self.haici_window)  # 切换到海词窗口
            #
            # time.sleep(1)
            #
            # # Change haici title
            # self.driver.execute_script("document.title = '海词词典识别'")

            return True

        except:
            logger.error('登录 扇贝出错')
            sys.exit(-1)

    def close_previous(self):
        """关闭上一次打开的扇贝窗口"""
        previous1 = pyautogui.getWindowsWithTitle(self.browser_title1)
        if len(previous1) > 0:
            logger.debug('关闭上一次打开的扇贝窗口')
            pyautogui.getWindowsWithTitle(self.browser_title1)[0].close()  # 先关闭已存在的浏览器

        previous2 = pyautogui.getWindowsWithTitle(self.browser_title2)
        if len(previous2) > 0:
            logger.debug('关闭上一次打开的扇贝窗口')
            pyautogui.getWindowsWithTitle(self.browser_title2)[0].close()  # 先关闭已存在的浏览器

        previous3 = pyautogui.getWindowsWithTitle(self.browser_title3)
        if len(previous3) > 0:
            logger.debug('关闭上一次打开的扇贝窗口')
            pyautogui.getWindowsWithTitle(self.browser_title3)[0].close()  # 先关闭已存在的浏览器

    def show(self):
        """最大化窗口然后激活"""
        maxed = False
        try:
            pyautogui.getWindowsWithTitle(self.browser_title1)[0].maximize()
            pyautogui.getWindowsWithTitle(self.browser_title1)[0].activate()
            maxed = True
        except:
            pass

        try:
            pyautogui.getWindowsWithTitle(self.browser_title2)[0].maximize()
            pyautogui.getWindowsWithTitle(self.browser_title2)[0].activate()
            maxed = True
        except:
            pass

        try:
            pyautogui.getWindowsWithTitle(self.browser_title3)[0].maximize()
            pyautogui.getWindowsWithTitle(self.browser_title3)[0].activate()
            maxed = True
        except:
            pass

        if not maxed:
            raise Exception('没有找到扇贝窗口')
