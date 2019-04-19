import pygame

pygame.init()

def text(DISPLAYSURF,X,Y,size,color,text, anchor = "topleft", render = True):
   BASICFONT = pygame.font.Font('freesansbold.ttf', size)
   Text = BASICFONT.render(str(text), True, color)
   TextRect = Text.get_rect()
   exec("TextRect.%s = (X,Y)"%anchor)
   if render:
       DISPLAYSURF.blit(Text,TextRect)
   return TextRect

class Drop_Down:
    def __init__(self, pos, options, surface, color = (255, 255, 255), color2 = (150, 150, 150), text_size = 17, index = 0, width = 75, height = 30):
        self.pygame = pygame
        self.pos = pos
        self.options = options
        self.index = index
        self.text_size = text_size
        self.height = height
        self.width = width
        self.rect = pygame.Rect(*pos, width, self.height * len(options))
        self.lines = []
        self.mode = 0
        self.surface = surface
        self.text = text
        self.rects = []
        self.color = color
        self.color2 = color2
        for x in range(len(options)):
            self.lines.append(((pos[0], pos[1] + (x * self.height)), (self.rect.right, pos[1] + (x * self.height))))
            self.rects.append(pygame.Rect(pos[0], pos[1] + (height * x), width, height))

    def draw(self):
        if self.mode == 1:
            self.pygame.draw.rect(self.surface, self.color, self.rect)
            self.pygame.draw.rect(self.surface, self.color2, self.rects[self.index])
            for line in self.lines:
                self.pygame.draw.line(self.surface, (0, 0, 0), line[0], line[1])
            for text in self.options:
                self.text(self.surface, *self.rects[self.options.index(text)].center, self.text_size, (0, 0, 0), text, anchor = "center")
        if self.mode == 0: 
            self.pygame.draw.rect(self.surface, self.color2, self.rects[0])
            self.text(self.surface, *self.rects[0].center, self.text_size, (0, 0, 0), self.options[self.index], anchor = "center")

    def get_status(self):
        return self.options[self.index]

    def set_status(self, op):
        self.index = self.options.index(op)

    def events(self, event):
        mouse_rect = self.pygame.Rect(*self.pygame.mouse.get_pos(), 1, 1)
        if event.type == self.pygame.MOUSEBUTTONDOWN:
            if self.mode == 0:
                if self.rects[0].colliderect(mouse_rect):
                    self.mode = 1
            elif self.mode == 1:
                for rect in self.rects:
                    if rect.colliderect(mouse_rect):
                        self.mode = 0
                        self.index = self.rects.index(rect)
