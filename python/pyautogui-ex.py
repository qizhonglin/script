#!/usr/bin/env python

import pyautogui
pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

try:
	while True:
		x, y = pyautogui.position()
		positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
		print positionStr + ' '
except KeyboardInterrupt:
	print '\nDone.'
