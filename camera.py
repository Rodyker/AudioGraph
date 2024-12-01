import cv2
import numpy as np
from trace_points import trace
from output import Output

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

camera_res = (80, 60) # x, y
display_res = (320, 240) # x, y

camera_flip_x = True
camera_flip_y = False

#dsp 8+1

blur_size = 7 #odd numbers
#blur size speeds
#3: 4.5
#5: 3.5
#7: 2.3 - excessive lines
#9: 2.1 - basic facial features
#11:2.0 - mostly outline

audio_scaling = 3
#audio scaling sampling frequencies at blue size 9
#lower = more jumping, higher = more noise
#1: 5-10 ms/div 3ks minimum
#2: 5-10 ms/div 3ks minimum
#3: 10-20 ms/div 3ks minimum 3 w/ 10ms/div 3ks recomended
#4: 10 ms/div 3ks
#5+: 20 ms/div 3ks

output = Output(audio_scaling, flip_y= True, flip_x_y= True)

try:
    while True:
        ret, img = cap.read()

        if camera_flip_x:
            img = cv2.flip(img, 1)
        if camera_flip_y:
            img = cv2.flip(img, 0)

        small = cv2.resize(img, camera_res)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (blur_size, blur_size), 0)
        outline = cv2.Canny(blur, 10, 70)

        cv2.imshow('line', cv2.resize(outline, display_res))
        cv2.moveWindow('line', 0, 0)
        cv2.imshow('color', cv2.resize(img, display_res))
        cv2.moveWindow('color', 0, 400)
        
        if cv2.waitKey(1) == 13: break

        points = np.argwhere(outline>1)
        if len(points) == 0: continue

        output.sound_clear()
        for point in trace(points):
            output.sound_append(points[point][0] / camera_res[0], 
                               points[point][1] / camera_res[0])
        output.update_wave()
except KeyboardInterrupt:
    pass
finally:
    output.close()