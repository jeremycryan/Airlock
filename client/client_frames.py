#!/usr/bin/env python

import pygame
import sys

from constants import *

""" Prompts user for a server IP """
def ip_prompt():

    screen = pygame.display.set_mode([ALT_WINDOW_WIDTH,
                                      ALT_WINDOW_HEIGHT],
                                     pygame.FULLSCREEN)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill([100, 100, 100])
        pygame.display.flip()
        pass

if __name__ == "__main__":
    ip_prompt()
