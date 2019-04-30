#!/usr/bin/env python3

import sys
import time
import copy
import random
import pygame
from nachomines.scripts.auto_load import AutoLoad
from nachomines.scripts.Utils import *
from nachomines.scripts.button import Drop_Down
from nachomines import __version__
from pkg_resources import resource_filename

pygame.init()

gameName = "NachoMines"
__author__ = "NachoMonkey"

caption = f"{gameName} {__version__}"

DefaultDisplaySize = (1080, 1080)


def gray(v):
    return (v, v, v)

gridColor = gray(0)
gridColorDark = (175, 125, 0)

blockColor = gray(150)
blockColorHover = gray(130)
blockColorPressed = gray(80)
blockExplored = gray(200)
blockMine = (200, 0, 0)
blockColorsReg = [blockColor, blockColorHover,
        blockColorPressed, blockExplored, blockMine]
blockColorDark = gray(50)
blockColorDarkHover = gray(75)
blockColorDarkPressed = gray(30)
blockColorDarkExplored = gray(80)
blockColorsDark = [blockColorDark, blockColorDarkHover, blockColorDarkPressed,
        blockColorDarkExplored, blockMine]

blockColors = [blockColorsReg, blockColorsDark]

theColors = [0, (0, 0, 255),
        (255, 0, 0),
        (255, 150, 0),
        (0, 100, 0),
        (0, 255, 0),
        (0, 200, 200),
        (75, 50, 255),
        (255, 0, 255),
]

FPS = 25
Clock = pygame.time.Clock()

def getSquareDisplay(w, h):
    if w >= h:
        return (h, h)
    if h > w:
        return (w, w)

def getGridRects(w, h, blockSize):
    for y in range(h):
        for x in range(w):
            yield pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)

def getGridLines(w, h, blockSize):
    X = []
    Y = []
    starts = []
    ends = []
    for x in range(w):
        X.append(x * blockSize)
    for y in range(h):
        Y.append(y * blockSize)
    for x in X:
        starts.append((x, 0))
        ends.append((x, h * blockSize))
    for y in Y:
        starts.append((0, y))
        ends.append((w * blockSize, y))
    return list(zip(starts, ends))

Info = pygame.display.Info()

class Game:
    def __init__(self, again=False):
        self.won = False
        self.lost = False
        self.playing = False
        self.started = False
        if again:
            return
        self.width, self.height = self.size = getSquareDisplay(Info.current_w,
                Info.current_h)
        self.Display = pygame.display.set_mode(self.size, pygame.FULLSCREEN, 32)
        pygame.display.set_caption(caption)

        icon = pygame.image.load(resource_filename("nachomines", "icon.png"))
        pygame.display.set_icon(icon)

        self.Scaling = Scaling(self.Display.get_size(), DefaultDisplaySize)
        self.scale = self.Scaling.scale_pos
        self.scaleX = self.Scaling.scale_singleX
        self.scaleY = self.Scaling.scale_singleY

        loader = AutoLoad()
        self.images = self.Scaling.scale_images(loader.Start_AutoLoad())

        self.subDropDown = Drop_Down(self.scale((100, 600)), list(range(5, 19)),
                self.Display, color2 = gray(100))
        self.minesDropDown = Drop_Down(self.scale((200, 600)), list(range(5, 76, 5)),
                self.Display, color2 = gray(100))
        self.themeDropDown = Drop_Down(self.scale((300, 600)), ["Light", "Dark"],
                self.Display, color2 = gray(100))
        self.subDropDown.set_status(10)
        self.minesDropDown.set_status(25)
        self.themeDropDown.set_status("Dark")
        self.dark_theme = True

    def recalc(self):
        self.dark_theme = self.themeDropDown.get_status() == "Dark"
        self.GridSub = self.subDropDown.get_status()
        self.BlockAmount = self.GridSub ** 2
        self.Mines = int(self.minesDropDown.get_status() / 100 * self.BlockAmount)
        self.BlockSize = self.Display.get_width() // self.GridSub

        self.images["flag"] = pygame.transform.smoothscale(self.images["flag"],
                (self.BlockSize, self.BlockSize))
        self.images["mine"] = pygame.transform.smoothscale(self.images["mine"],
                (self.BlockSize, self.BlockSize))
        self.blocks = []
        self.gridLines = getGridLines(self.GridSub, self.GridSub, self.BlockSize)
        for r in getGridRects(self.GridSub, self.GridSub, self.BlockSize):
            self.blocks.append(Block(r, self.images["flag"], self.images["mine"], self.dark_theme))
        self.flags = 0

    def main(self):
        while True:
            self.draw()
            self.events()
            self.update()

    def exit(self):
        print(f"{red}Exiting...{endC}")
        pygame.quit()
        sys.exit()

    def generateBoard(self, clicked, block):
        usedMines = 0
        newBlocks = copy.copy(self.blocks)
        stop = False
        while not stop:
            for b in self.blocks:
                if random.randint(0, self.BlockAmount) == self.blocks.index(b)\
                        and not newBlocks[self.blocks.index(b)].hasMine\
                        and not b.rect.collidepoint(clicked):
                    newBlocks[self.blocks.index(b)].hasMine = True
                    usedMines += 1
                    if usedMines == self.Mines:
                        stop = True
                        break
        for b in newBlocks:
            bordering = 0
            for B in self.getBordering(b):
                if B.hasMine:
                    bordering += 1
            newBlocks[newBlocks.index(b)].surrounding = bordering
        self.explore(block)
        self.blocks = newBlocks
        self.started = True

    def explore(self, block):
        if not block.hasMine:
            block.statusL = 3
            block.flagged = False
        for b in self.getBordering(block):
            if not b.hasMine:
                b.statusL = 3
                block.flagged = False
                b.flagged = False
                b.explored += 1
            if b.surrounding == 0 and b.explored < 2 and not b.hasMine:
                self.explore(b)

    def getBordering(self, block):
        r = block.rect.inflate(block.rect.w * 1.25, block.rect.h * 1.25)
        border = []
        for b in self.blocks:
            if b.rect.colliderect(r) and b != block:
                border.append(b)
        return border

    def drawGrid(self, grid):
        for g in grid:
            pygame.draw.aaline(self.Display, [gridColor, gridColorDark][self.dark_theme], g[0], g[1], 2)

    def draw(self):
        if self.playing:
            self.draw_game()
        else:
            self.draw_menu()

    def draw_menu(self):
        self.Display.blit(self.images["MainMenu"], (0, 0))
        self.subDropDown.draw()
        self.minesDropDown.draw()
        self.themeDropDown.draw()

        Adv_Fonts(self.scale((90, 580)),
        self.Display, self.scaleY(15), "Grid Subdivisions",
        color = (255, 255, 0), font = "freesansbold", bold = True, anchor = "topleft")
        
        Adv_Fonts(self.scale((200, 580)),
        self.Display, self.scaleY(15), "Mine Density",
        color = (255, 255, 0), font = "freesansbold", bold = True, anchor = "topleft")

        Adv_Fonts(self.scale((300 + self.scaleX(75 / 2), 580)),
        self.Display, self.scaleY(15), "Theme",
        color = (255, 255, 0), font = "freesansbold", bold = True, anchor = "midtop")

        Adv_Fonts((self.Display.get_width() // 2, self.Display.get_height() // 2),
                self.Display, self.scaleY(50), "Press Enter to Continue",
                color = (255, 255, 0), font = "monospace", bold = True)

        Adv_Fonts((self.Display.get_width() // 2, self.Display.get_height() - self.scaleY(100)),
                self.Display, self.scaleY(20), "Press <R> to regenerate board",
                color = (255, 255, 0), font = "monospace", bold = True)



    def draw_game(self):
        for b in self.blocks:
            b.draw(self.Display)
        self.drawGrid(self.gridLines)
        text = ""
        color = (0, 0, 0)
        if self.won or self.lost:
            rect = pygame.Rect((0, 0), (self.Display.get_width() // 1.25,
                self.Display.get_height() // 3))
            rect.center = self.Display.get_rect().center
            pygame.draw.rect(self.Display, gray(0), rect.move(2, 4))
            pygame.draw.rect(self.Display, gray(45), rect)
            text = ["You Hit A Mine!!", "You Won!!!"][self.won]
            color = [(255, 0, 0), (0, 200, 0)][self.won]
        Adv_Fonts((self.Display.get_width() // 2, self.Display.get_height() // 2),
                self.Display, self.scaleY(75), text, color = color,
                font = "monospace", bold = True, shadow = True)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not self.playing:
                        self.playing = True
                        self.recalc()
                    if self.lost or self.won:
                        self.__init__(True)
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.exit()
                if event.key == pygame.K_r and self.playing:
                    self.__init__(True)
                    self.playing = True
                    self.recalc()
            if not self.playing:
                self.minesDropDown.events(event)
                self.subDropDown.events(event)
                self.themeDropDown.events(event)

    def update(self):
        if self.playing and not self.won and not self.lost:
            pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            mines = 0
            self.flags = 0
            if True:
                for b in self.blocks:
                    self.flags += b.flagged
                    if b.statusL != 3:
                        b.update(pos, click[0], 0)
                        b.update(pos, click[2], 1)
                        if b.upStatL and not b.flagged:
                            if not self.started:
                                self.generateBoard(pos, b)
                            else:
                                if not b.hasMine:
                                    self.explore(b)
                                else:
                                    b.statusL = 4
                                    self.lost = True
                        if b.upStatR and self.started and self.flags < self.Mines:
                            b.flagged = not b.flagged
                    if b.hasMine:
                        mines += 1
                    if b.flagged and b.hasMine:
                        mines -= 1
                    if b.flagged and not b.hasMine:
                        mines += 2
            if mines == 0 and self.started:
                self.won = True
        pygame.display.update()
        Clock.tick(FPS)

class Block:
    def __init__(self, rect, flag, mine, dark):
        self.rect = rect
        self.dark = dark
        self.statusL = 0                           # 0 = normal, 1 = hover, 2 = click, 3 = explored, 4 = HIT MINE
        self.statusR = 0
        self.hasMine = 0
        self.explored = 0
        self.clickL = False
        self.clickR = False
        self.upStatL = False
        self.upStatR = False
        self.flagged = False
        self.updated = False
        self.surrounding = 0
        self.flag = flag
        self.mine = mine

    def draw(self, display):
        pygame.draw.rect(display, blockColors[self.dark][self.statusL], self.rect)
        if self.flagged:
            fr = self.flag.get_rect()
            fr.center = self.rect.center
            display.blit(self.flag, fr)
        if self.statusL == 4:
            mr = self.mine.get_rect()
            mr.center = self.rect.center
            display.blit(self.mine, mr)
        if self.statusL == 3 and self.surrounding != 0 and not self.hasMine:
            Adv_Fonts(self.rect.move(0, 2).center, display, self.rect.h, self.surrounding,
                    font = "monospace", color=(0, 0, 0))
            Adv_Fonts(self.rect.center, display, self.rect.h, self.surrounding,
                    font = "monospace", color = theColors[self.surrounding])

    def update(self, pos, click, left):            # Left: 0 for left click, 1 for right click
        if left == 0:
            self.upStatL = False
        if left == 1:
            self.upStatR = False
        stat = copy.copy([self.statusL, self.statusR])[left]
        c = copy.copy([self.clickL, self.clickR])[left]
        coll = False
        if self.updated:
            coll = self.rect.collidepoint(pos)
            if not coll:
                stat = 0
            else:
                if (not c and click):
                    stat = 2
                if not click:
                    stat = 1
        else:
            self.updated = True
        if left == 0:
            if not click and self.clickL and coll and self.statusL:
                self.upStatL = True
            self.clickL = click
            self.statusL = stat
        if left == 1:
            if not click and self.clickR and coll and self.statusR:
                self.upStatR = True
            self.clickR = click
            self.statusR = stat

def run():
    g = Game()
    g.main()
