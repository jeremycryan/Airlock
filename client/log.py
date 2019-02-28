#!/usr/bin/env python

from constants import *

#   Outside libraries
import pygame

class Log(object):
    """ Prints events that occur in an event log on the sidebar. """

    def __init__(self, screen):

        #   Initialize width and height
        self.width = LOG_WIDTH
        self.height = LOG_HEIGHT

        #   List of surfaces for the log to blit
        self.lines = []

        #   Font
        self.font = LOGFONT
        self.font_size = 15
        self.font_obj = pygame.font.Font(self.font, self.font_size)

        #   Typesetting
        self.line_break = 20
        self.line_spacing = 0

        #   Position parameters
        self.xpos = LOG_XPOS
        self.ypos = LOG_YPOS

        #   Pygame surface
        self.screen = screen
        self.surf = pygame.Surface((self.width, self.height)).convert()
        self.surf.set_alpha(150)


    def add_line(self, text):
        """ Generates surfaces for the message. """

        words = text.split()
        num_to_try = len(words)

        while len(words) > 0:

            #   Stop the loop if you can't fit a single word on the line.
            if num_to_try == 0:
                break

            text_to_try = " ".join(words[:num_to_try])
            surf = self.generate_font(text_to_try)

            #   Try again with less of the message if it's too wide
            if surf.get_width() > self.width:
                num_to_try -= 1
                continue

            #   Add the text to the lines to render
            self.lines.append(surf)

            if num_to_try < len(words):
                words = words[num_to_try:]
                num_to_try = len(words)
            else:
                break

    def draw(self):
        """ Draws the text of the log on the screen. """

        self.surf.fill(pygame.SRCALPHA)

        text_yoff = len(self.lines) * self.line_break

        ypos = 0
        for idx, line in enumerate(self.lines):
            ypos = self.height - text_yoff + (idx) * self.line_break
            self.surf.blit(line, (0, ypos))

        #   Blit the surface onto the passed screen.
        self.screen.blit(self.surf, (self.xpos, self.ypos))

    def generate_font(self, text, color=(255, 255, 255)):
        """ Generates a surface for a string. """

        string = self.font_obj.render(text, 1, color)
        return string
