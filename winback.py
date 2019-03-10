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
		self.setGeometry(300, 300, 300, 300)
		self.label = QLabel("Drag an image file here.", self)
		self.label.move(100,150)			
	
	def dragEnterEvent(self, e):
	  
		if e.mimeData():
			e.accept()
		else:
			e.ignore() 

	def dropEvent(self, e):
		img_path = e.mimeData().text().split("file:///")[1]
		self.dual_1080p_4K_backg_conv(img_path)
		
	# Function to convert image to dual 1080p and 4K monitor desktop backgrounds
	def dual_1080p_4K_backg_conv(self, img_path):
		
		# If the IMAGE PATH actually exists as a file...
		if os.path.isfile(img_path):
			self.update_label(self.label.text() + "\nIMAGE PATH exists. Attempting to open image...")
			self.update()
			img = Image.open(img_path)
			width, height = img.size
			
			# Force 7680 x 2160 dimensions (might look ugly for some images)
			if (width, height) != (7680, 2160):
				self.update_label(self.label.text() + "\nImage isn't 7680x2160. Resizing image to 7680x2160...")
				img = img.resize((7680, 2160), Image.ANTIALIAS)
				
			self.update_label(self.label.text() + "\nProcessing image...")
			
			cropped_img = img.crop((0,0,3840,2160))
			cropped_img = cropped_img.resize((1920,1080))

			final_img = img.crop((1920,0,7680,2160))
			final_img.paste(cropped_img)
			
			# Use source file as basis for name of final image file (replace file extension with "-WINBACK.jpeg")
			final_img_save_path = img_path[:img_path.rfind(".")] + "-WINBACK.jpeg"
			self.update_label(self.label.text() + "\nNew image created: %s" % final_img_save_path)
			final_img.save(final_img_save_path, quality=90)

			self.set_windows_background(final_img_save_path)
				
		# Else, the IMAGE PATH didn't actually exist.
		else:
			self.update_label(self.label.text() + "\nFILE ERROR: File does not exist.")
			
	def set_windows_background(self, file_path):
		# Check to make sure that we're running on Windows and that file_path exists
		if os.name == "nt" and os.path.isfile(file_path):
			import ctypes
			#ctypes.windll.user32.SystemParametersInfoW(20, 0, final_img_save_path, 0)
			SPI_SETDESKWALLPAPER = 20
			SPIF_UPDATEINIFILE = 1
			user32 = ctypes.WinDLL('user32', use_last_error=True)

			def errcheck(result, func, args):
				if not result:
					raise ctypes.WinError(ctypes.get_last_error())
				return args
			
			user32.LoadStringW.errcheck = errcheck
			
			user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, file_path, SPIF_UPDATEINIFILE)
			self.label.setText(self.label.text() + "\nDesktop background set.")
			
		# Else, the file_path didn't actually exist.
		else:
			self.label.setText(self.label.text() + "OS ERROR: Can only set desktop background on Windows.")
			
	def update_label(self, str=None):
		if str is not None:
			print(str + "\n")
			self.label.setText(str)
			self.repaint()
			obj = self
			for attr in dir(obj):
				print("obj.%s = %r" % (attr, getattr(obj, attr)))
			# self.label.setText(str)
			# self.label.repaint()
			# self.label.show()

if __name__ == '__main__':
  
	app = QApplication([])
	ui = Winback()
	ui.show()
	exit(app.exec_())	 