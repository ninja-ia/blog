import numpy as np
import cv2 
import ctypes as ct
from ctypes import *
import math
import random
import libreria as lib

# Carga la red, los pesos y las etiquetas
net = lib.load_net(b"/home/user/darknet/cfg/yolov3.cfg", b"/home/user/darknet/yolov3.weights",0);
meta = lib.load_meta(b"/home/user/darknet/cfg/coco.data");
  
# Lee el video y calcula el número total de frames 
video = cv2.VideoCapture("./video.mp4") 
number = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# Podemos definir desde qué frame y hasta cuál queremos ir acá (si queremos ir al último usamos ultimo = number)
primero = 0
ultimo = 10
currentframe = primero

print('\n'+'DETECCION USANDO DARKNET + YOLOV3')
print('\n'+'Cantidad de frames totales = ',number)
print('\n'+'Primer frame = ',primero,'\n' + 'Ultimo frame =',ultimo)
print('\n' + '\n' )

# Corre la red para los frames seleccionados
while currentframe < ultimo:
    
    video.set(1,currentframe)
    ret,framevid = video.read()
    print(currentframe)  
    
    if ret: 
        
        imagerot = lib.rotateimage(framevid,90) # Puede ser necesario rotar los frames del video
        r = lib.detect(net, meta, imagerot); # Procesado de la red
        print(r)
        print('###########################################################################')
    
        
    else: 
        break
    
    currentframe = currentframe + 1
 
    
# Libera el video
video.release() 


