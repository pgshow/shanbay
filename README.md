# Shanbay Bot
This bot can help you make custom English dictionary on 扇贝 very convenient.
Login in Shanbay.com automatically, Quickly snapshot the subtitle on the PotPlayer and 51talk class by click mouse middle button, then use Baidu OCR API to get the text and search the text on Shanbay.com directly.

# 准备
- 自建 keys 文件夹
- 修改 account.py 内容成你的，然后放入 keys 文件夹

### 使用流程:

1.运行 1aunch.bat

2.程序会自动登录扇贝，请提前设置你的账号密码

3.PotPlayer 播放美剧时，空格键暂停美剧，然后点击鼠标中键可以出现截图框。

4.出现截图框后，单击鼠标左键在字幕上拖动可以对单词截图，或者按 ESC 键取消截图。

5.浏览器自动激活，在扇贝搜索该单词/词组。

6.然后你可以看到单词解释，以及最重要的 '加入单词本功能'。

7.加入单词本的单词你可以在扇贝的手机APP里面学习，此法边看美剧边学单词方便又快捷。

### 注意
- 需要等待 Selenium 自动登录扇贝，否则点击鼠标中键没有任何反应

## 更新
### 2022-10-01
- 增加 51talk 上课软件的截屏搜词功能