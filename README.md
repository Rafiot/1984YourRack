Keep an eye on your rack when you are not around.

# Installation

Please run ./src/install_deps.sh

# Blockers

On rpi armv6 pillow has issues:

```
(myPiMotion) pi@camepi:~/code/1984YourRack $ ./src/myPiMotion.py
Traceback (most recent call last):
  File "./src/myPiMotion.py", line 8, in <module>
    from PIL import Image
  File "/home/pi/code/1984YourRack/myPiMotion/lib/python3.5/site-packages/PIL/Image.py", line 60, in <module>
    from . import _imaging as core
ImportError: libopenjp2.so.7: cannot open shared object file: No such file or directory
```

libopenjp2.so.7 is usually provided by libopenjp2-7-dev but is not in the current sources.
