#!/usr/bin/env python

################## WINDOW AND RESOLUTION SETTINGS #####################

#   Size of the window, in pixels
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
MID_X = int(WINDOW_WIDTH/2)
MID_Y = int(WINDOW_HEIGHT/2)

################## CARD OBJECT SETTINGS ###############################

#   Size of the cards, in pixels
CARDSIZE = (80, 112)
CARD_WIDTH = CARDSIZE[0]
CARD_HEIGHT = CARDSIZE[1]


################# DECK OBJECT SETTINGS ################################

#   Vertical and horizontal offset of card number
DECK_XOFF = 0
DECK_YOFF = int(CARD_HEIGHT/3)
DECK_STAGGER = 2

################# PLAYER SUMMARY OBJECT SETTINGS ######################

#   Spacing and overall offset of player summary cards
PLAYER_SPACING = 25
PLAYER_X = 30
PLAYER_Y = 50
PLAYER_WIDTH = 260
PLAYER_HEIGHT = 200

#   Offsets for character card
CHAR_X = CARDSIZE[0] + PLAYER_SPACING + PLAYER_X
CHAR_Y = PLAYER_Y

#   Offsets for mission card
MISS_X = PLAYER_X
MISS_Y = PLAYER_Y

#   Maximum rectangle of user interface, including player summaries
PLAYER_REGION_X = WINDOW_WIDTH * 0.125   #   offset from screen center
PLAYER_REGION_Y = 0     #   offset from screen center
PLAYER_REGION_HEIGHT = WINDOW_HEIGHT * 0.9
PLAYER_REGION_WIDTH = WINDOW_WIDTH * 0.7

#   Easier-to-work-with variables
PR_LX = PLAYER_REGION_X + MID_X - int(PLAYER_REGION_WIDTH/2)
PR_RX = PLAYER_REGION_X + MID_X + int(PLAYER_REGION_WIDTH/2)
PR_TY = PLAYER_REGION_Y + MID_Y - int(PLAYER_REGION_HEIGHT/2)
PR_BY = PLAYER_REGION_Y + MID_Y + int(PLAYER_REGION_HEIGHT/2)
PR_MX = PLAYER_REGION_X + MID_X
PR_MY = PLAYER_REGION_Y + MID_Y

#   Player default positions
PLAYER_POSITIONS = {1: (PR_LX, PR_TY),
    2: (PR_LX, PR_MY - int(PLAYER_HEIGHT/2)),
    3: (PR_LX, PR_BY - PLAYER_HEIGHT),
    4: (PR_RX - PLAYER_WIDTH, PR_TY),
    5: (PR_RX - PLAYER_WIDTH, PR_MY - int(PLAYER_HEIGHT/2)),
    6: (PR_RX - PLAYER_WIDTH, PR_BY - PLAYER_HEIGHT)}

################## OXYGEN OBJECT SETTINGS #############################

#   Position of the center of the oxygen cells on the screen
OXYGEN_POS = (PLAYER_REGION_X + MID_X,
    PLAYER_REGION_Y + MID_Y)
OXYGEN_SPACING = 20

################# PILE LAYOUT #########################################

#   Define position of draw and discard piles, relative to oxygen
PILE_OFFSET = 30
PILE_02_OFFSET = 30
DRAW_PILE_POS = (int(PR_MX + PILE_OFFSET/2),
    int(OXYGEN_POS[1] - CARD_HEIGHT * 1.5 - PILE_02_OFFSET))

################# SIDEBAR SETTINGS ####################################

SIDEBAR_WIDTH = WINDOW_WIDTH * 0.25
SIDEBAR_X_MARG = 20
SIDEBAR_Y_MARG = 50

################# FONTS ###############################################

CARDFONT = "None"
DECKFONT = "None"
