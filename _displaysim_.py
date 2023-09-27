import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import cv2
import numpy as np

class Screen:
    def __init__(self):
        self.frameSize = (128, 64)
        self.xyCoord = [10, 0]
        self.isUp = True
        self.timeCheck = time.time()
        self.colors = ["red", "orange", "yellow", "green", "blue", "magenta", "white", "cyan"]
        self.color = 0
        self.state = None
        
    def _updateImage(self, image=None):
        if image:
            npImage = np.asarray(image)
            frameBGR = cv2.cvtColor(npImage, cv2.COLOR_RGB2BGR)
            cv2.imshow('Test', frameBGR)
            self.state = image
        else:
            image = Image.new('RGB', self.frameSize, 'white')
            font = ImageFont.truetype("freefont-ttf/sfd/FreeMonoBold.ttf", 12)
            draw = ImageDraw.Draw(image)
            draw.rectangle([(0, 0), (self.frameSize[0] - 1, self.frameSize[1] - 1)], 'black', 'white')
            npImage = np.asarray(image)
            frameBGR = cv2.cvtColor(npImage, cv2.COLOR_RGB2BGR)
            cv2.imshow('Test', frameBGR)
            self.state = image
        
    def _drawText(self, text, cord, color, size=12):
        image = Image.new('RGB', self.frameSize, 'white')
        font = ImageFont.truetype("freefont-ttf/sfd/FreeMonoBold.ttf", size)
        draw = ImageDraw.Draw(image)

        draw.rectangle([(0, 0), self.frameSize[0] - 1, self.frameSize[1] - 1], 'black', 'white')
        draw.text(cord, text, fill=self.colors[color], font=font)
        self._updateImage(image)


    def test(self):
        while True:
            self._drawText("Hello World", self.xyCoord, self.color)
            if self.isUp:
                self.xyCoord[1] += 1
            else:
                self.xyCoord[1] -= 1
            
            if self.xyCoord[1] == self.frameSize[1] - 13:
                self.isUp = False
                self.color += 1
            elif self.xyCoord[1] == 0:
                self.isUp = True
                self.color += 1
            
            if self.color == len(self.colors):
                self.color = 0
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        self.closeScreen()

    def closeScreen(self):
        cv2.destroyAllWindows()

class ScrollableScreen(Screen):
    def __init__(self, menuItems, fontSize=12):
        super().__init__()
        self.menuItems = menuItems
        self.listOffset = 0
        self.fontHeight = fontSize
        self.highlightedIndex = 0
        self.visible_items = self.frameSize[1] // self.fontHeight

    def _draw(self):
        image = Image.new('RGB', self.frameSize, 'black')
        font = ImageFont.truetype("freefont-ttf/sfd/FreeMonoBold.ttf", self.fontHeight)
        draw = ImageDraw.Draw(image)

        y_position = 0
        for idx, string in enumerate(self.menuItems[self.listOffset:]):
            if y_position + self.fontHeight > self.frameSize[1]:
                break

            if idx + self.listOffset == self.highlightedIndex:

                draw.rectangle([(10, y_position + 3), (self.frameSize[0] - 10, y_position + self.fontHeight + 3)], fill='white')
                draw.text((10, y_position), string, fill='black', font=font)
            else:
                draw.text((10, y_position), string, fill='white', font=font)
            y_position += self.fontHeight

            total_height = len(self.menuItems) * self.fontHeight
            visible_height = self.frameSize[1]
            scrollbar_total_height = visible_height
            scrollbar_visible_height = visible_height * visible_height / total_height
            scrollbar_position = (self.listOffset * self.fontHeight * scrollbar_total_height) / total_height
            draw.rectangle([(self.frameSize[0] - 3, 0), (self.frameSize[0], scrollbar_total_height)], outline='white')
            draw.rectangle([(self.frameSize[0] - 3, scrollbar_position), (self.frameSize[0], scrollbar_position + scrollbar_visible_height)], fill='white')

            self._updateImage(image)

    def displayStringList(self):
        self._draw()
        while True:
            k = cv2.waitKeyEx(1)
            if k == 27:
                break
            elif k == 13:
                self.closeScreen()
                return self.highlightedIndex
            elif k == 2621440:  # Down arrow key
                if self.highlightedIndex < len(self.menuItems) - 1:
                    self.highlightedIndex += 1
                if self.highlightedIndex >= self.listOffset + self.visible_items:
                    self.listOffset += 1
                self._draw()
            elif k == 2490368:  # Up arrow key
                if self.highlightedIndex > 0:
                    self.highlightedIndex -= 1
                if self.highlightedIndex < self.listOffset:
                    self.listOffset -= 1
                self._draw()

        self.closeScreen()


if __name__ == "__main__":
    screen = Screen()
    screen.test()
    items = ["Settings", "WiFi", "SubGHz", "NFC", "RFID", "Infrared", "USB"]
    menu = ScrollableScreen(items)
    selection = menu.displayStringList()
    print(items[selection])
