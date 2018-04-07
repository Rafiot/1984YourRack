Keep an eye on your rack when you are not around.

# Python3 only

Python 2, thank you for your years of faithful service.

Python 3, your time is now.

[Python 2.7 will retire in…](https://pythonclock.org/)

# Installation

Please run ./src/install_deps.sh

# Issues

On rpi armv6l pillow had issues:

```
(myPiMotion) pi@camepi:~/code/1984YourRack $ ./src/myPiMotion.py
Traceback (most recent call last):
  File "./src/myPiMotion.py", line 8, in <module>
    from PIL import Image
  File "/home/pi/code/1984YourRack/myPiMotion/lib/python3.5/site-packages/PIL/Image.py", line 60, in <module>
    from . import _imaging as core
ImportError: libopenjp2.so.7: cannot open shared object file: No such file or directory
```

libopenjp2.so.7 is usually provided by libopenjp2-7-dev and pillow needs other dependencies install, install_deps.sh does this for you.

```
sudo apt install -y libopenjp2-7-dev libtiff5-dev libatlas-base-dev
```
