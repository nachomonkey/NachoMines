#!/usr/bin/env python3

import sys
import time
import copy
import random
import os
import pygame

pygame.init()

def get_square_display(w, h):
    return (min(w, h), ) * 2 

info = pygame.display.Info()
margin = 50
width, height = size = get_square_display(info.current_w - margin, info.current_h - margin)
os.environ["SDL_VIDEO_WINDOW_POS"] = f"{info.current_w // 2 - width // 2}, {info.current_h // 2 - height // 2}"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from nachomines.scripts.auto_load import AutoLoad
from nachomines.scripts.get_file import get_file
from nachomines.scripts.utils import *
from nachomines.scripts.button import Drop_Down
from nachomines import __version__
from pygame.mixer import Sound

gameName = "NachoMines"
__author__ = "NachoMonkey"

caption = f"{gameName}"

DefaultDisplaySize = (1080, 1080)

def playSound(filename):
    Sound(fix_path(get_file("resources/sounds/" + filename))).play()

def gray(v):
    return (v, v, v)

gridColor = gray(0)
gridColorDark = (175, 125, 0)
gridColorNacho = (255, 255, 0)

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

FPS = 60
Clock = pygame.time.Clock()

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

class Game:
    def __init__(self, again=False):
        self.won = False
        self.lost = False
        self.playing = False
        self.started = False
        self.mseg_alpha = 255
        self.mseg = None
        if again:
            return
        self.Display = pygame.display.set_mode(size, pygame.NOFRAME | pygame.HWACCEL)
        pygame.display.set_caption(caption)

        icon = pygame.image.load(get_file("icon.png"))
        pygame.display.set_icon(icon)

        self.Scaling = Scaling(self.Display.get_size(), DefaultDisplaySize)
        self.scale = self.Scaling.scale_pos
        self.scaleX = self.Scaling.scale_singleX
        self.scaleY = self.Scaling.scale_singleY

        loader = AutoLoad()
        self.old_images = self.Scaling.scale_images(loader.Start_AutoLoad())
        self.images = copy.copy(self.old_images)

        self.subDropDown = Drop_Down(self.scale((width / 2 - 238, 600)), list(range(5, 19)),
                self.Display, color2 = gray(100))
        self.minesDropDown = Drop_Down(self.scale((width / 2 - 38, 600)), list(range(5, 76, 5)),
                self.Display, color2 = gray(100))
        self.themeDropDown = Drop_Down(self.scale((width / 2 + 162, 600)), ["Light", "Dark", "Nacho"],
                self.Display, color2 = gray(100))
        self.subDropDown.set_status(10)
        self.minesDropDown.set_status(25)
        self.themeDropDown.set_status("Dark")

        self.time_passed = 0
        self.event_time = 0
        self.dirty_rects = []

    def recalc(self):
        self.theme = self.themeDropDown.get_status()
        self.GridSub = self.subDropDown.get_status()
        self.BlockAmount = self.GridSub ** 2
        self.Mines = int(self.minesDropDown.get_status() / 100 * self.BlockAmount)
        self.BlockSize = self.Display.get_width() // self.GridSub
        f_name = "flag"
        m_name = "mine"
        if self.theme == "Nacho":
            f_name = "spicy_alert"
            m_name = "jalapeno"

        self.images[f_name] = pygame.transform.smoothscale(self.old_images[f_name],
                (self.BlockSize, self.BlockSize))
        self.images[m_name] = pygame.transform.smoothscale(self.old_images[m_name],
                (self.BlockSize, self.BlockSize))
        if self.theme == "Nacho":
            self.images["chip1"] = pygame.transform.smoothscale(self.old_images["chip1"],
                    (self.BlockSize, self.BlockSize))
            self.images["chip2"] = pygame.transform.smoothscale(self.old_images["chip2"],
                    (self.BlockSize, self.BlockSize))
        self.blocks = []
        self.gridLines = getGridLines(self.GridSub, self.GridSub, self.BlockSize)
        for r in getGridRects(self.GridSub, self.GridSub, self.BlockSize):
            chip = None
            if self.theme == "Nacho":
                name = random.choice(["chip1", "chip2"])
                chip = pygame.transform.flip(self.images[name], random.randint(0, 1), random.randint(0, 1))
            self.blocks.append(Block(r, self.images[f_name], self.images[m_name], chip, self.theme, self.dirty_rects))
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
            block.is_dirty = True
        for b in self.getBordering(block):
            if not b.hasMine:
                b.statusL = 3
                block.flagged = False
                b.flagged = False
                b.explored += 1
                b.is_dirty = True
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
        color = gridColorDark
        if self.theme == "Light":
            color = gridColor
        if self.theme == "Dark":
            color = gridColorDark
        if self.theme == "Nacho":
            color = gridColorNacho
        for g in grid:
            pygame.draw.aaline(self.Display, color, g[0], g[1], 2)

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

        render_text(self.subDropDown.rects[0].midtop,
        self.Display, self.scaleY(15), "Grid Subdivisions",
        color = (255, 255, 0), font="freesansbold", bold=True, anchor="midbottom")
        
        render_text(self.minesDropDown.rects[0].midtop,
        self.Display, self.scaleY(15), "Mine Density",
        color = (255, 255, 0), font="freesansbold", bold=True, anchor="midbottom")

        render_text(self.themeDropDown.rects[0].midtop,
        self.Display, self.scaleY(15), "Theme",
        color = (255, 255, 0), font="freesansbold", bold=True, anchor="midbottom")

        render_text((round(self.Display.get_width() * (9/10)), round(self.Display.get_height() * (9/10))),
                self.Display, self.scaleY(14), f"v{__version__}",
                color=(255, 255, 255), font="monospace", anchor="bottomright")

        render_text((self.Display.get_width() // 2, self.Display.get_height() - self.scaleY(100)),
                self.Display, self.scaleY(20), "Press <R> to restart",
                color=(255, 255, 0), font="monospace", bold=True, shadow=True)
        pygame.display.update()


    def draw_game(self):
        for b in self.blocks:
            b.draw(self.Display)
        self.drawGrid(self.gridLines)
        text = ""
        color = (0, 0, 0)
        if self.won or self.lost:
            if not self.mseg:
                self.mseg = self.Display.copy()
            mseg_surf = self.mseg.copy()
            rect = pygame.Rect((0, 0), (self.Display.get_width() // 1.75,
                self.Display.get_height() // 4))
            rect.center = self.Display.get_rect().center
            pygame.draw.rect(mseg_surf, gray(0), rect.move(2, 4))
            pygame.draw.rect(mseg_surf, gray(45), rect)
            color = [(255, 0, 0), (0, 200, 0)][self.won]
            img = self.images["you_lost" if self.lost else "mines_cleared"]
            r = img.get_rect()
            r.center = rect.center
            mseg_surf.blit(img, r)
            mseg_surf.set_alpha(self.mseg_alpha)
            self.Display.blit(mseg_surf, (0, 0))
            self.event_time -= self.time_passed
            self.dirty_rects.append(rect.inflate(50, 50))
            if self.event_time < 0 and self.mseg_alpha > 0:
                self.mseg_alpha -= 150 * self.time_passed
            if self.mseg_alpha < 0:
                self.__init__(True)
                self.mseg_alpha = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.lost or self.won:
                        self.__init__(True)
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
            for b in self.blocks:
                self.flags += b.flagged
                if b.statusL != 3:
                    b.update(pos, click[0], 0)
                    b.update(pos, click[2], 1)
                    if b.upStatL and not b.flagged:
                        if not self.started:
                            playSound("click.wav")
                            self.generateBoard(pos, b)
                            pygame.display.update()
                        else:
                            if not b.hasMine:
                                playSound("click.wav")
                                self.explore(b)
                            else:
                                b.statusL = 4
                                self.lost = True
                                self.event_time = 2
                                playSound("boom.wav")
                    if b.upStatR and self.started and self.flags < self.Mines:
                        if b.flagged:
                            playSound("remove_flag.wav")
                        if not b.flagged:
                            playSound("add_flag.wav")
                        b.flagged = not b.flagged
                if b.hasMine:
                    mines += 1
                if b.flagged and b.hasMine:
                    mines -= 1
                if b.flagged and not b.hasMine:
                    mines += 2
            if mines == 0 and self.started:
                playSound("success.wav")
                self.won = True
                self.event_time = 2
        pygame.display.update(self.dirty_rects)
        self.dirty_rects.clear()
        self.time_passed = Clock.tick(FPS) / 1000

class Block:
    def __init__(self, rect, flag, mine, chip, theme, dirty_rects):
        self.rect = rect
        self.chip = chip
        self.theme = theme
        self.dark = False if theme == "Light" else True
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
        self.clicked = False
        self.surrounding = 0
        self.flag = flag
        self.mine = mine
        self.dirty_rects = dirty_rects
        self.is_dirty = True
        self.last_hover = False
        self.last_click = False

    def draw(self, display):
        if self.is_dirty:
            self.is_dirty = False
            self.dirty_rects.append(self.rect)
        pygame.draw.rect(display, blockColors[self.dark][self.statusL], self.rect)
        if self.chip and not (self.clicked or self.explored):
            cr = self.chip.get_rect()
            cr.center = self.rect.center
            display.blit(self.chip, cr)
        if self.flagged:
            fr = self.flag.get_rect()
            fr.center = self.rect.center
            display.blit(self.flag, fr)
        if self.statusL == 4:
            mr = self.mine.get_rect()
            mr.center = self.rect.center
            display.blit(self.mine, mr)
            self.dirty_rects.append(self.rect)
        if self.statusL == 3 and self.surrounding != 0 and not self.hasMine:
            render_text(self.rect.move(0, 2).center, display, round(self.rect.h * .6), self.surrounding,
                    font="georgia", color=(0, 0, 0))
            render_text(self.rect.center, display, round(self.rect.h * .6), self.surrounding,
                    font="georgia", color=theColors[self.surrounding])

    def update(self, pos, click, left):            # Left: 0 for left click, 1 for right click
        if self.upStatL:
            self.clicked = True
        if left == 0:
            self.upStatL = False
        if left == 1:
            self.upStatR = False
        stat = copy.copy([self.statusL, self.statusR])[left]
        c = copy.copy([self.clickL, self.clickR])[left]
        coll = self.rect.collidepoint(pos)
        if self.last_hover != coll:
            self.is_dirty = True
        self.last_hover = coll
        if self.last_click != click and coll:
            self.is_dirty = True
        self.last_click = click

        if self.updated:
            if not coll:
                stat = 0
            else:
                if (not c and click):
                    stat = 2
                if not click:
                    stat = 1
        else:
            self.updated = True
        sl = self.statusL
        sr = self.statusR
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
    print("\n--NachoMonkey--")
    print("   presents")
    print(f"NachoMines v{__version__} \n")
    try:
        g = Game()
        g.main()
    except KeyboardInterrupt:
        print()
