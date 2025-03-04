import time, pyautogui

for i in range(300):

	print(i)

	# Delay for 5 seconds
	time.sleep(10)

	# Capture the screenshot
	screenshot = pyautogui.screenshot()
	screenshot.save(f"/Users/lanting/Downloads/screenshot/{i+155}.png")

	# next page
	pyautogui.press('right')

