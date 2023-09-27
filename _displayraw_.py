import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import cv2
import numpy as np 
'''  # Import Luma.OLED libraries  from luma.core.interface.serial import spi  from luma.oled.device import ssd1331  # Configure the serial port  serial = spi(device=0, port=0)  device = ssd1331(serial)  '''    

def main():
    frameSize = (128, 64)
    xyCoord = [10,0]
    isUp = True
    timeCheck = time.time()
    colors = ["red", "orange", "yellow", "green", "blue"
              , "magenta", "white", "cyan"
    ]
    color = 0
    time.sleep(0.1)
    while 1:
        image = Image.new('RGB', (frameSize), 'white')
        font = ImageFont.truetype("freefont-ttf/sfd/FreeMonoBold.ttf", 12)
        draw = ImageDraw.Draw(image)
        if isUp:
            xyCoord[1] += 1          
        else:              
            xyCoord[1] -= 1                        
        if xyCoord[1] == frameSize[1] - 13:              
            isUp = False              
            color += 1          
        elif xyCoord[1] == 0:              
            isUp = True              
            color += 1                        
        if color == len(colors):              
            color = 0            
            draw.rectangle([(0,0), (frameSize[0] - 1, frameSize[1] - 1)], 'black', 'white')          
            draw.text((xyCoord), 'Hello World', fill=colors[color], font=font)          
            time.sleep(0.01)          
            fps = "FPS: {0:0.3f}".format(1/(time.time() - timeCheck))          
            timeCheck = time.time()          
            draw.text((2, 0), fps, fill='white')                    
            '''          # Output to OLED display          device.display(image)          '''            # Virtual display          
            npImage = np.asarray(image)          
            frameBGR = cv2.cvtColor(npImage, cv2.COLOR_RGB2BGR)          
            cv2.imshow('Test', frameBGR)          
            k = cv2.waitKey(1) & 0xFF          
            if k == 27:              
                break            # Virtual display      
    cv2.destroyAllWindows()              
if __name__ == "__main__":      
    main()