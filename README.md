# winback
GUI that allows you to drag an image to be set as a dual-monitor background in Windows. Currently only works for unique dual-monitor setup where left monitor is 1080p (1920x1080) and right monitor is 4K (3840x2160), therefore causing Windows not to span dual-monitor desktop background images correctly. Works best with images that are 7680x2160 (image will be scaled to this size regardless of original size). Currently considering expanding functionality for more use cases.

## Requirements
Python 3.5+\
PyQt5 version 5.9.2

## Setup
Install latest Python for Windows (be sure to check the box on the first install screen that says **Add Python 3.x to PATH**)\
Open Windows Command Prompt (type `cmd.exe` in Start)\
Type `python -m pip install PyQt5==5.9.2`\
Double-click on *winback.pyw* to start application
