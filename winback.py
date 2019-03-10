# Imported packages
import os
import sys
from PIL import Image

# Function to convert image to dual 1080p and 4K monitor desktop backgrounds
def dual_1080p_4K_backg_conv(argv):

	# There should be exactly two arguments: winback.py and "IMAGE PATH"
	if len(argv) != 2:
		print("Invalid command. Usage:")
		print("\tpython winback.py \"IMAGE PATH\" (incl. quotes)")
		print("Now exiting.")
		exit(2)
	
	# Assign the IMAGE PATH to a variable
	img_path = argv[1]

	# If the IMAGE PATH actually exists...
	if os.path.exists(img_path):
		print("IMAGE PATH exists. Attempting to open image...")
		img = Image.open(img_path)
		width, height = img.size
		
		if (width, height) != (7680, 2160):
			print("Image isn't 7680x2160. Resizing image to 7680x2160...")
			img = img.resize((7680, 2160), Image.ANTIALIAS)
			
		print("Processing image...")
		
		cropped_img = img.crop((0,0,3840,2160))
		cropped_img = cropped_img.resize((1920,1080), Image.ANTIALIAS)

		final_img = img.crop((1920,0,7680,2160))
		final_img.paste(cropped_img)
		final_img_save_path = img_path[:img_path.rfind(".")] + "-WINBACK.jpeg"
		print("New image created: %s" % final_img_save_path)
		final_img.save(final_img_save_path)

		if os.name == "nt":
			import ctypes
			ctypes.windll.user32.SystemParametersInfoW(20, 0, final_img_save_path, 0)
			
	# Else, the IMAGE PATH didn't actually exist.
	else:
		print("The IMAGE PATH entered does not exist. Usage:")
		print("\tpython winback \"IMAGE PATH\" (incl. quotes)")
		print("Now exiting.")
		exit(2)
	

# "Main" function calls the function above.
if __name__ == '__main__':
	# Pass sys.argv (all arguments passed to "python") to function
	dual_1080p_4K_backg_conv(sys.argv)