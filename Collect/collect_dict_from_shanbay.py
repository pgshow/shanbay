# 收集扇贝单词本中的所有单词
# 需要手动登录，以及选择单词本中今日新词，今日复习，在学单词，未学单词，简单词等
# 注意每个单词分类的第一页可能会被遗漏，跟流程有关，可以手动加一下第一页的单词
import time
from safe_driver import SafeDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    driver = SafeDriver().driver
    driver.get('https://web.shanbay.com/web/account/login/')
    print('Waiting for login...')
    time.sleep(20)
    driver.get('https://web.shanbay.com/wordsweb/#/words-table')
    print('Please choose the right cards table...')
    time.sleep(10)
    print('Start collecting...')

    previous_top_word = ''
    while 1:

        try:
            for i in range(10):
                # Wait for the top word to change, which means the ajax is loaded
                current_top_word = driver.find_element(By.XPATH, "//div[contains(@class, 'index_wordsInner__')]/div/div[1]")
                if current_top_word != previous_top_word:
                    previous_top_word = current_top_word
                    break
                time.sleep(1)

            words = driver.find_elements(By.XPATH, "//div[contains(@class, 'index_wordsInner__')]/div/div[1]")
            for word in words:
                print(word.text)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li[text()='下一页']")))

            # Check if the next page button is clickable

            driver.find_element(By.XPATH, "//li[text()='下一页']").click()
            time.sleep(1)
        except Exception as e:
            # print(e)
            print('--------------------Error-----------------------')
            time.sleep(10)
