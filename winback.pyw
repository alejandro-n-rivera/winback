import os
import sys
import time
from PIL import Image
from PyQt5.QtWidgets import QLabel, QWidget, QApplication

class Winback(QWidget):
  
	def __init__(self):
		super().__init__()
		self.setAcceptDrops(True)
		self.initUI()
		
	def initUI(self):
		self.setWindowTitle('winback')
		self.label = QLabel("Drag an image file here.", self)
		self.setGeometry(300, 300, 300, 300)
		self.label.move(100,150)
		
	# Function to convert image to dual 1080p and 4K monitor desktop backgrounds
	def dual_1080p_4K_backg_conv(self, img_path):
		
		# If the IMAGE PATH actually exists...
		if os.path.exists(img_path):
			self.label.setText(self.label.text() + "\nIMAGE PATH exists. Attempting to open image...")
			img = Image.open(img_path)
			width, height = img.size
			
			# Force 7680 x 2160 dimensions (might look ugly for some images)
			if (width, height) != (7680, 2160):
				self.label.setText(self.label.text() + "\nImage isn't 7680x2160. Resizing image to 7680x2160...")
				img = img.resize((7680, 2160), Image.ANTIALIAS)
				
			self.label.setText(self.label.text() + "\nProcessing image...")
			
			cropped_img = img.crop((0,0,3840,2160))
			cropped_img = cropped_img.resize((1920,1080), Image.ANTIALIAS)

			final_img = img.crop((1920,0,7680,2160))
			final_img.paste(cropped_img)
			
			# Use source file as basis for name of final image file (replace file extension with "-WINBACK.jpeg")
			final_img_save_path = img_path[:img_path.rfind(".")] + "-WINBACK.jpeg"
			self.label.setText(self.label.text() + "\nNew image created: %s" % final_img_save_path)
			final_img.save(final_img_save_path)

			if os.name == "nt":
				import ctypes
				ctypes.windll.user32.SystemParametersInfoW(20, 0, final_img_save_path, 0)
				self.label.setText(self.label.text() + "\nDesktop background set.")
				
		# Else, the IMAGE PATH didn't actually exist.
		else:
			self.label.setText(self.label.text() + "\nFile error: File does not exist\nNow exiting...")
			time.sleep(3)
			exit(2)
			
	
	def dragEnterEvent(self, e):
	  
		if e.mimeData():
			e.accept()
		else:
			e.ignore() 

	def dropEvent(self, e):
		img_path = e.mimeData().text()
		img_path = img_path.split("file:///")[1]
		self.dual_1080p_4K_backg_conv(img_path)


if __name__ == '__main__':
  
	app = QApplication(sys.argv)
	wb = Winback()
	wb.show()
	app.exec_()	 