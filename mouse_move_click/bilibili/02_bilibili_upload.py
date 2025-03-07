# bilibili 稿件删除
import pyautogui as pg
import time

# 获取鼠标位置的坐标值
# time.sleep(2)
# mouse_x, mouse_y = pg.position()
# print("鼠标位置的坐标值:", mouse_x, mouse_y)

def upload_mp4_on_bilibili():

	# 方向键移动都窗口最下面
	pg.press('down', presses = 10)

	# 因为可能位置会上下移动一点所以多个位置
	time.sleep(1)
	pg.click(x=740, y=950)
	time.sleep(10)


i = 0

while True:
	if i == 5:
		time.sleep(60)
		i = 0
	else:
		upload_mp4_on_bilibili()
		i+=1