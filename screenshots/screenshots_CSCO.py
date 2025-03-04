import time, pyautogui

cover_page = 1 # 默认是2(看自己想把哪一页作为目录页)
start_page = 5 # 目录的页码(直接输入即可)

time.sleep(3)

# turn to cover_page
pyautogui.press('backspace')
pyautogui.press('backspace')
pyautogui.press('backspace')
pyautogui.typewrite(str(cover_page),interval=0.2)

pyautogui.press('enter')

# Delay for 5 seconds
time.sleep(1)

# Capture the screenshot
screenshot = pyautogui.screenshot()
screenshot.save(f"/Users/lanting/Downloads/screenshot/0.png")

for i in range(700):
	num = i + start_page
	print(num)

	# turn to page
	pyautogui.press('backspace')
	pyautogui.press('backspace')
	pyautogui.press('backspace')
	pyautogui.typewrite(str(num),interval=0.2)
	pyautogui.press('enter')

	# Delay for 5 seconds
	time.sleep(1)

	# Capture the screenshot
	screenshot = pyautogui.screenshot()
	screenshot.save(f"/Users/lanting/Downloads/screenshot/{num}.png")




