import time
import pyautogui
from loguru import logger

click_time = []
click_location = []
click_count = 1
path_clicked = {}
time_difference = 0
count = 1


def single_double_click(x, y):
    """
    判断鼠标是单击还是双击
    :return 1 or 2  单击或双击
    """
    global count
    global click_count
    global time_difference  # 把时间差设为全局变量 为的是退出这个循环

    path_infor = {}
    t = time.time()
    click_time.append(t)  # 添加时间
    click_location.append((x, y))  # 添加位置

    if len(click_location) != 1:
        time_difference = click_time[1] - click_time[0]  # 定义时间差

        if click_location[0] == click_location[1]:
            if time_difference <= 0.3:  # 如果两次点击时间小于0.3秒就会判断为双击 否则就是单击
                click_count = 2
            else:
                click_count = 1
        else:
            click_count = 1

        click_time.pop(0)  # 删去第一个
        click_location.pop(0)
        if click_count == 2:  # 双击时 第一次击中的记录需要删去 否则执行的时候会是单击即使两个单击时间间隔很短 还有时间记录的得是上一次的
            time_difference = path_clicked[count - 1]['time_interval']
            count = count - 1

    # 记录行为
    path_infor['x'] = x
    path_infor['y'] = y
    path_infor['click_count'] = click_count
    path_infor['time_interval'] = round(time_difference, 2)

    print('Released at {0} at {1} 点击次数{2}'.format(x, y, click_count))
    path_clicked[count] = path_infor
    count = count + 1

    return click_count


def is_long_press(pressTime):
    """是否长按"""
    hold_time = time.time() - pressTime
    if hold_time >= 1.2:
        logger.info('监测到 PotPlayer 长按')
        return True
