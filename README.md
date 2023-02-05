# BinaryEye-to-remote-numpad-server
Send barcodes from BinaryEye to the computer as HID via remote-numpad-server (Wifi)
Barcodes are types like from the keyboard.

Limitations
-----------
*Unmodified*, remote-numpad-server can be used only with numeric barcodes (EAN13, EAN8...)  
Alphanumeric barcodes are not supported (CODE128, QRCODE...)  
A modified version allowing other HID keystroke is possible but security concerns may appears as some alphanumeric barcodes could permit to send malicious keystrokes.

# Installation
Download and install [remote-numpad-server](https://github.com/theolizard/remote-numpad-server) on your PC  
Download and install [BinaryEye](https://github.com/markusfisch/BinaryEye) on your Android device  
Download be2rns.py

# Configuration

be2rns.py
---------
You can change the default port in the beginning of the file or add it on command line.  
Make it executable or you can run it with python3.  
Don't forget to open you firewall if needed for this port.  

BinaryEye
---------
In Preferences:  
- Activate `Forward scans`  
- URL to forward to: Give the address of your be2rns server on your PC (something like `http://192.168.1.10:4577`)  
- Request type: `POST application/json`  

# How to use it
- Start remote-numpad-server on your PC  
- Start be2rns.py in a console or as a service `python3 ./be2rns.py`  
- Use BinaryEye normally on your Android device


Thanks and all credits to @theolizard and @markusfisch for their respective software.  
This little script is just a glue between them.
Enjoy :)

