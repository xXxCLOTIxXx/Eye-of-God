import pyautogui
import cv2, numpy
from datetime import datetime
from win32api import GetSystemMetrics
from threading import Thread
from tkinter import Tk, Button, Label
from tkinter.messagebox import showerror

class App:
	def __init__(self, mode: str = 'Normal', run: bool = True):
		self.size = {'top': 0, 'left': 0, 'width': GetSystemMetrics(0), 'height': GetSystemMetrics(1)}
		self.title = "Eye of God"
		self.mode = mode
		self.run = run
		if run:Thread(target=self.main).start()

		#ui
		self.window = Tk()
		self.window.title(self.title)
		self.window.geometry('350x150')

	def get_time(self):
		return str(datetime.now())

	def change_mode(self, lbl):
		if self.mode == 'Normal':self.mode='Gray'
		else:self.mode='Normal'
		lbl.configure(text=f"Режим отображения: {self.mode}")

	def change_cam(self, lbl):
		if self.run == True:self.run=False
		else:
			self.run=True
			Thread(target=self.main).start()
		lbl.configure(text=f"Камера активна: {self.run}")

	def UI(self):
		lbl_mode = Label(self.window, text=f"Режим отображения: {self.mode}", font=("Arial Bold", 15))
		lbl_cam = Label(self.window, text=f"Камера активна: {self.run}", font=("Arial Bold", 15))  

		btn_mode = Button(self.window, text="Изменить цветовой режим", command=lambda: self.change_mode(lbl_mode))  
		btn_cam = Button(self.window, text="Отключить / включить камеру", command=lambda: self.change_cam(lbl_cam)) 

		btn_mode.grid(column=0, row=0, pady=10)
		btn_cam.grid(column=0, row=1)
		lbl_mode.grid(column=0, row=2, padx=30)
		lbl_cam.grid(column=0, row=3)
		self.window.mainloop()

	def main(self):
		try:
			cap = cv2.VideoCapture(1)
			#faice = cv2.CascadeClassifier('scales/trained.xml')
			while self.run:
				ret, image = cap.read()
				#resize = cv2.resize(image, (self.size['width'], self.size['height']))
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

				#faice_results = faice.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
				if self.mode == 'Normal':cv2.imshow(self.title, image)
				if self.mode == 'Gray':cv2.imshow(self.title, gray)
				if cv2.waitKey(25):
					pass
		except Exception as error:
			showerror('CamError', f'Произошла ошибка камеры:\n{error}')


if __name__ == '__main__':
	app=App()
	app.UI()