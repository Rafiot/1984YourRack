#!/usr/bin/env python

import sys
if sys.version_info[0] < 3:
    print("Must be using Python 3")
    sys.exit(-1)

import picamera
try:
    from io import StringIO
except:
    from io import StringIO
from PIL import Image
import time
import numpy


homedir = '/home/pi/'

width = 1296
height = 972

motion_width = 96
motion_height = 72
old_motion_hist = None
sensivity_day = 15
sensivity_night = 50
pictures_count = 2
threshold_brightness_day = motion_width * motion_height * 0.75
threshold_brightness_night = motion_width * motion_height * 0.75
is_night = False


def capture_motion_image(camera):
    image_data = StringIO()
    camera.capture(image_data, 'jpeg', use_video_port=True,
                   resize=(motion_width, motion_height))
    image_data.seek(0)
    im = Image.open(image_data).histogram()
    image_data.close()
    return im


def test_darkness(camera):
    image_data = StringIO()
    camera.capture(image_data, 'jpeg', use_video_port=True,
                   resize=(motion_width, motion_height))
    image_data.seek(0)
    im = Image.open(image_data)
    im_black_white = im.convert('1')
    px = list(im_black_white.getdata())
    if not is_night:
        print(px.count(0))
        return px.count(0) > threshold_brightness_day
    else:
        print(px.count(255))
        return px.count(255) < threshold_brightness_night


def test_motion(camera):
    global old_motion_hist
    new_motion_hist = capture_motion_image(camera)
    if old_motion_hist is None:
        # init capture
        old_motion_hist = new_motion_hist
        return False
    diff_squares = [(old_motion_hist[i] - new_motion_hist[i]) ** 2
                    for i in range(len(old_motion_hist))]
    rms = numpy.sqrt(sum(diff_squares) / len(old_motion_hist))
    old_motion_hist = new_motion_hist
    if is_night:
        sensivity = sensivity_night
    else:
        sensivity = sensivity_day
    if rms > sensivity:
        print(rms)
        night_switch(camera)
        return True
    return False


def night_switch(camera):
    global is_night
    if test_darkness(camera):
        if not is_night:
            print('This is night')
            is_night = True
            cam.exposure_mode = "night"
            cam.image_effect = "denoise"
            #cam.exposure_compensation = 25
            #cam.ISO = 800
            #cam.brightness = 75
            #cam.contrast = 50
    else:
        if is_night:
            print('Night is over')
            is_night = False
            #cam.contrast = 0
            #cam.brightness = 50
            #cam.ISO = 0
            #cam.exposure_compensation = 0
            cam.image_effect = "none"
            cam.exposure_mode = "auto"


def record(camera):
    try:
        print('start recording')
        count = pictures_count
        for i, f in enumerate(camera.capture_continuous('{timestamp}_{counter}.jpg')):
            print((i, f))
            count -= 1
            if count == 0:
                if not test_motion(camera):
                    print('it stopped moving')
                    return True
                count = pictures_count

    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    print('Starting')
    with picamera.PiCamera() as cam:
        cam.resolution = (width, height)
#        cam.framerate = 1
        print('Camera getting ready')
        time.sleep(2)
        print('Camera ready')
        while True:
            try:
                if test_motion(cam):
                    print('Got a move')
                    if not record(cam):
                        break
                else:
                    time.sleep(1)
            except KeyboardInterrupt:
                print('closing')
                break
            except Exception as e:
                print('Test motion failed')
                print(e)
                break
