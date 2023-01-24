import pyautogui
import cv2, numpy
from datetime import datetime
from win32api import GetSystemMetrics
from threading import Thread
from tkinter import Tk, Button, Label
from tkinter.messagebox import showerror
from random import choice

class App:
	def __init__(self, color_mode: str = 'Normal', AI: bool = True, wCams: int = 1, shooting: bool = True):

		#shooting - сьемка видео с камер (True / False)
		#wCams - количество камер (True / False)
		#AI - использовать искуственный инелект (True / False)
		#color_mode - цветовой режим ('Normal' / 'Gray')

		self.size = {'top': 0, 'left': 0, 'width': GetSystemMetrics(0), 'height': GetSystemMetrics(1)}
		self.title = "Eye of God"
		self.wCams = wCams
		self.shooting = shooting
		self.color_mode = color_mode
		self.view_mode = 'all'
		self.select_cam = 4
		self.cam_size = (400, 400)

		self.run = True
		self.use_AI = AI
		Thread(target=self.main).start()

		#ui
		self.window = Tk()
		self.window.title(self.title)
		self.window.geometry('350x280')
		self.window.resizable(width=False, height=False)
		self.window.attributes("-topmost",True)

	def get_time(self):
		return str(datetime.now())

	def change_mode(self, lbl):
		if self.color_mode == 'Normal':self.color_mode='Gray'
		else:self.color_mode='Normal'
		lbl.configure(text=f"Режим отображения: {self.color_mode}")

	def close(self):
		self.run=False
		exit()

	def change_selected(self, type: str):
		if type == 'up':
			if self.select_cam+1<5:self.select_cam+=1
			else:self.select_cam=0
		elif type == 'down':
			if self.select_cam-1<0:self.select_cam=self.wCams-1
			else:self.select_cam-=1


	def change_view_mode(self, lbl):
		if self.view_mode == 'solo':self.view_mode='all'
		else:self.view_mode='solo'
		lbl.configure(text=f"Режим отображения: {self.view_mode}")

	def UI(self):

		Button(self.window, text="<", command=lambda: self.change_selected('down')).grid(column=0, row=0)
		Button(self.window, text=">", command=lambda: self.change_selected('up')).grid(column=0, row=1)

		lbl_mode = Label(self.window, text=f"Режим отображения: {self.color_mode}", font=("Arial Bold", 15));lbl_mode.grid(column=0, row=5, padx=30)
		cam_mode = Label(self.window, text=f"Режим просмотра камер: {self.view_mode}", font=("Arial Bold", 15));cam_mode.grid(column=0, row=6, padx=30)
		Label(self.window, text=f"Всего камер: {self.wCams}", font=("Arial Bold", 15)).grid(column=0, row=7, padx=30)

		Button(self.window, text="Изменить цветовой режим", command=lambda: self.change_mode(lbl_mode)).grid(column=0, row=2, pady=10)
		Button(self.window, text="Изменить режим просмотра", command=lambda: self.change_view_mode(cam_mode)).grid(column=0, row=3, pady=10)
		Button(self.window, text="Закрыть", command=self.close).grid(column=0, row=4)

		self.window.mainloop()

	def AI(self, image, detected):
		for (x, y, h, w) in detected:
			cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
			cv2.putText(image, f'HUMAN',(x, y), cv2.FONT_HERSHEY_DUPLEX, 0.45, (200, 200, 200), 1)

		return image

	def redact(self, image, detect, ret = None, color = (100, 0, 0)):
		if ret==False:color=(255,255,255)
		else:
			if self.color_mode == 'Gray':color=(0, 0, 0)
			if self.use_AI:self.AI(image, detect)

		if self.view_mode != 'all':cv2.putText(image, f'CAMERA: {self.select_cam}',(10, 80), cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2)

		cv2.putText(image, f'TIME: {self.get_time()}',(10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2)

		if self.shooting:self.rec(image)
		return image

	def rec(self, image):
		pass

	def main(self):
		try:
			faice = cv2.CascadeClassifier('scales/trained.xml')

			cams = []
			for i in range(self.wCams):
				cap = cv2.VideoCapture(i)
				cams.append(cap)

			while self.run:
				if self.view_mode == 'solo':
					ret, image = cams[self.select_cam].read()
					if ret != True and self.view_mode == 'solo':image = cv2.imread('images/no_signal.jpg', cv2.IMREAD_GRAYSCALE)

				if self.view_mode == 'all':
					imgs = []
					for web in cams:
						ret, newImage = web.read()
						if ret != True:newImage = numpy.zeros((480,480,3), numpy.uint8)
						newImage = cv2.resize(newImage, self.cam_size)
						imgs.append(newImage)
					image = numpy.concatenate(imgs, axis=1)
					ret=None
				else:
					image = cv2.resize(image, (self.size['width'], self.size['height']))

				if ret !=False:
					gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
					faice_results = faice.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
				else:
					gray = image
					faice_results = ()
				if self.color_mode == 'Normal':
					cv2.imshow(self.title, self.redact(image, faice_results, ret))
				if self.color_mode == 'Gray':cv2.imshow(self.title, self.redact(gray, faice_results, ret))
				if cv2.waitKey(25):
					pass
		except Exception as error:
			showerror('CamError', f'Произошла ошибка камеры:\n{error}')


if __name__ == '__main__':
	app=App(wCams=5)
	app.UI()