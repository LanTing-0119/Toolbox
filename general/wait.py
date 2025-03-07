#进入待分类文件夹
import os,shutil
import binpacking
import sys,time,pyautogui,os
import tkinter 
from tkinter.messagebox import *
import time
from natsort import natsorted
import sys

def sleep(sleeptime):

    time.sleep(2)

    for i in range(int(sleeptime/4)):
        print(i)
        pyautogui.click(x=1000, y=600)
        time.sleep(3)
        pyautogui.click(x=1000, y=800)
        time.sleep(3)


        # pyautogui.click(x=1400, y=400)
        # time.sleep(30)
        # pyautogui.click(x=1400, y=200)
        # time.sleep(30)
        # pyautogui.typewrite('y')
        # time.sleep(5)
        # pyautogui.press('enter')
        # time.sleep(5)


sleep(1000000)

print('hello')