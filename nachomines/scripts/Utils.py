import pygame
import sys
import os

pygame.init()


red = "\033[91m"
blue = "\033[94m"
green = "\033[92m"
warn = "\033[93m"
endC = "\033[0m"

if sys.platform != "linux":
    red = ""
    blue = ""
    green = ""
    warn = ""
    endC = ""

def reverseDict(D):
    return dict(zip(D.values(), D.keys()))

def fixPath(path):
    return path.replace("/", os.sep)

def fixTime(t):
    if len(t) == 1:
        return "0" + t
    return t

def GenerateBars(barImage, amount, pos, Display = False, endTop = None, endBottom = None):
    firstRect = pygame.Rect((0, 0), barImage.get_size())
    firstRect.center = (pos[0], pos[1])
    bars = []
    if endTop:
        topRect = pygame.Rect((0, 0), endTop.get_size())
        topRect.bottom = firstRect.top
        topRect.centerx = firstRect.centerx
        bars.append(topRect.topleft)
    for Bar in range(amount):
        bars.append((firstRect.topleft[0], firstRect.topleft[1] + (firstRect.height * Bar)))
    if endBottom:
        botRect = pygame.Rect((0, 0), endTop.get_size())
        botRect.bottom = (firstRect.topleft[1] + (firstRect.height * amount))
        botRect.centerx = firstRect.centerx
        bars.append(botRect.topleft)
    if Display:
        if endTop:
            Display.blit(endTop, bars[0])
        for Bar in bars[1:-1]:
            Display.blit(barImage, Bar)
        if endBottom:
            Display.blit(endBottom, bars[-1])

def stereo_pan(sound, x, width):
    right = x / width
    left = 1 - right
    if sound:
        sound.set_volume(left, right)

def stereo_pan_normal(x, width):
    right = x / width
    left = 1 - right
    return (left, right)

def Adv_Fonts(pos, display, size, text, font = "Sans", color = (0, 0, 0),  italic = False, bold = False, AA = True, underline = False, anchor = "center", render = True, shadow = False, shadowDistance = 2):
    rfont = pygame.font.SysFont(font, size)
    rfont.set_italic(italic)
    rfont.set_bold(bold)
    rfont.set_underline(underline)
    Text = rfont.render(str(text), AA, color)
    TextRect = Text.get_rect()
    exec("TextRect.%s = pos" % anchor)
    if shadow:
        font2 = pygame.font.SysFont(font, size)
        font2.set_italic(italic)
        font2.set_bold(bold)
        font2.set_underline(underline)
        Text2 = font2.render(str(text), AA, (0, 0, 0))
        TextRect2 = Text2.get_rect()
        Pos2 = (pos[0] + shadowDistance, pos[1] + shadowDistance)
        exec("TextRect2.%s = Pos2" % anchor)
    if render:
        if shadow:
            display.blit(Text2, TextRect2)
        display.blit(Text, TextRect)
    return (Text, TextRect)

class Scaling:
    def __init__(self, DisplaySize, default = (1920, 1080)):
        self.DisplaySize = DisplaySize
        self.default = default

    def get_ratio(self, size):
        return (size[0] / self.default[0], size[1] / self.default[1])

    def scale_pos(self, pos, R = True):
        ratio = self.get_ratio(self.DisplaySize)
        a1 = pos[0] * ratio[0]
        a2 = pos[1] * ratio[1]
        if R:
            a1 = round(a1)
            a2 = round(a2)
        return (a1, a2)

    def scale_singleX(self, num, R = True):
        a = self.get_ratio(self.DisplaySize)[0] * num
        if R: a = round(a)
        return a

    def scale_singleY(self, num, R = True):
        a = self.get_ratio(self.DisplaySize)[1] * num
        if R: a = round(a)
        return a

    def scale_single(self, num):
        ratio = self.get_ratio(self.DisplaySize)
        return num * round((ratio[0] + ratio[1]) / 2)

    def scale_image(self, image):
        if self.DisplaySize == self.default:
            return image
        ratio = self.get_ratio(self.DisplaySize)
        size = image.get_size()
        New = pygame.transform.scale(image, (round(size[0] * ratio[0]), round(size[1] * ratio[1])))
        return New

    def scale_images(self, images):
        if self.DisplaySize == self.default:
            return images
        imgs = []
        ratio = self.get_ratio(self.DisplaySize)
        for img in images:
            Img = images[img]
            size = Img.get_size()
            New = pygame.transform.scale(Img, (round(size[0] * ratio[0]), round(size[1] * ratio[1])))
            imgs.append(New)
        return dict(zip(list(images.keys()), imgs))

    def scale_images2(self, images):
        if self.DisplaySize == self.default:
            return images
        imgs = []
        ratio = self.get_ratio(self.DisplaySize)
        for img in images:
            Img = images[images.index(img)]
            size = Img.get_size()
            New = pygame.transform.scale(Img, (round(size[0] * ratio[0]), round(size[1] * ratio[1])))
            imgs.append(New)
        return imgs

