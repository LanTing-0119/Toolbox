# bilibili 稿件删除
import pyautogui as pg
import time

# 获取鼠标位置的坐标值
# time.sleep(2)
# mouse_x, mouse_y = pg.position()
# print("鼠标位置的坐标值:", mouse_x, mouse_y)

def delete_mp4_on_bilibili():
	# 1523,400
	pg.moveTo(x=1523, y=390)
	time.sleep(2)
	# 1292,628 # 删除
	pg.click(x=1292, y=628)
	time.sleep(5)
	# 823,575 # 验证
	pg.click(x=823, y=575)
	time.sleep(5)

# file_num = 60
# for i in range(file_num):
# 	print(i)

time.sleep(1)
while True:
	delete_mp4_on_bilibili()