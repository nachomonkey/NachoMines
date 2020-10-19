import os
import pygame
from nachomines.scripts.utils import green, endC, fix_path
from nachomines.scripts.get_file import get_file

pygame.init()

path = get_file("resources/images/bitmap/")

class AutoLoad:
    def __init__(self):
        self.names = []
        self.images = []

    def remove_extension(self, filename):
        return filename[:filename.index(".")]

    def Start_AutoLoad(self):
       for (root, dirs, files) in os.walk(path):
           for File in files:
               if not File.startswith("."):
                   self.names.append(self.remove_extension(File))
                   self.images.append(pygame.image.load(root + os.path.sep + File))
       final = dict(zip(self.names, self.images))
       return final
