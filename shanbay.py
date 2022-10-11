import sys
import time
import pyautogui
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
        self.browser_title = '扇贝，知道你在改变'
        self.driver = SafeDriver().driver
        self.login(self.driver)

    def search_word(self, word):
        """从扇贝搜索单词"""
        logger.info(f'搜索单词 {word}')

        driver = self.driver
        try:
            driver.get('https://web.shanbay.com/web/main/index')
            driver.find_element(By.CSS_SELECTOR, 'div.searchContainer > input').send_keys(word)
            time.sleep(1)
            # await asyncio.sleep(1)
            driver.find_element(By.CSS_SELECTOR, 'div.searchContainer .submit').click()
            # driver.maximize_window()
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
            return True

        except:
            logger.error('登录 扇贝出错')
            sys.exit(-1)

    def close_previous(self):
        """关闭上一次打开的扇贝窗口"""
        previous = pyautogui.getWindowsWithTitle(self.browser_title)
        if len(previous) > 0:
            logger.debug('关闭上一次打开的扇贝窗口')
            pyautogui.getWindowsWithTitle(self.browser_title)[0].close()  # 先关闭已存在的浏览器

    def show(self):
        """最大化窗口然后激活"""
        pyautogui.getWindowsWithTitle(self.browser_title)[0].maximize()
        pyautogui.getWindowsWithTitle(self.browser_title)[0].activate()
