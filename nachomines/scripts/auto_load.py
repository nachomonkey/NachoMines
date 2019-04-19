import os
import pygame
from nachomines.scripts.Utils import green, endC, fixPath
from pkg_resources import resource_filename

pygame.init()

path = resource_filename("nachomines", fixPath("resources/images/bitmap/"))

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
           print(f"{green}Collected {files} from {root}{endC}")
       final = dict(zip(self.names, self.images))
       return final
