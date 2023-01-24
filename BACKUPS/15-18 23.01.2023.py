import pyautogui
import cv2, numpy
from datetime import datetime
from win32api import GetSystemMetrics

size = {'top': 0, 'left': 0, 'width': GetSystemMetrics(0), 'height': GetSystemMetrics(1)}
title = "Minecraft fishing"
mode = 'Gray' # Gray

def get_time():
	return str(datetime.now()).split(':')[2].split('.')[0]


def main():
	cap = cv2.VideoCapture(1)
	#faice = cv2.CascadeClassifier('scales/trained.xml')

	while True:
		ret, image = cap.read()
		resize = cv2.resize(image, (size['width'], size['height']))
		gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)

		#faice_results = faice.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
		if mode == 'Normal':cv2.imshow(title, image)
		if mode == 'Gray':cv2.imshow(title, gray)
		if cv2.waitKey(25):
			pass


if __name__ == '__main__':
	main()