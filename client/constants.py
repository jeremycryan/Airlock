#!/usr/bin/env python

################## WINDOW AND RESOLUTION SETTINGS #####################

#   Size of the window, in pixels
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
ALT_WINDOW_WIDTH = 800
ALT_WINDOW_HEIGHT = 450
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
PLAYER_REGION_X = WINDOW_WIDTH * 0.11   #   offset from screen center
PLAYER_REGION_Y = 0     #   offset from screen center
PLAYER_REGION_HEIGHT = WINDOW_HEIGHT * 0.92
PLAYER_REGION_WIDTH = WINDOW_WIDTH * 0.73

#   Easier-to-work-with variables
PR_LX = PLAYER_REGION_X + MID_X - int(PLAYER_REGION_WIDTH/2)
PR_RX = PLAYER_REGION_X + MID_X + int(PLAYER_REGION_WIDTH/2)
PR_TY = PLAYER_REGION_Y + MID_Y - int(PLAYER_REGION_HEIGHT/2)
PR_BY = PLAYER_REGION_Y + MID_Y + int(PLAYER_REGION_HEIGHT/2)
PR_MX = PLAYER_REGION_X + MID_X
PR_MY = PLAYER_REGION_Y + MID_Y

#   Player default positions
PLAYER_POSITIONS = {3: (PR_LX, PR_TY),
    2: (PR_LX, PR_MY - int(PLAYER_HEIGHT/2)),
    1: (PR_LX, PR_BY - PLAYER_HEIGHT),
    4: (PR_RX - PLAYER_WIDTH, PR_TY),
    5: (PR_RX - PLAYER_WIDTH, PR_MY - int(PLAYER_HEIGHT/2)),
    6: (PR_RX - PLAYER_WIDTH, PR_BY - PLAYER_HEIGHT)}

#   Player name positions
PLAYER_NAME_POS = (0, 8)
PLAYER_HAND_POS = (0, 0)
PLAYER_HAND_SCALE = 0.7
PLAYER_HAND_YOFF = 0

#   Permanents settings
PERMANENTS_POS = (int(PLAYER_WIDTH/2), int(PLAYER_HEIGHT + CARD_WIDTH*0.2))
GLOBAL_PERM_POS = (100, 100)

################## OXYGEN OBJECT SETTINGS #############################

#   Position of the center of the oxygen cells on the screen
OXYGEN_POS = (PLAYER_REGION_X + MID_X,
    PLAYER_REGION_Y + MID_Y - 240)
OXYGEN_SPACING = 15

################# STAGE SETTINGS ######################################

STAGE_VERT_OFFSET = 100
STAGE_POS = (OXYGEN_POS[0], OXYGEN_POS[1] + STAGE_VERT_OFFSET + CARD_HEIGHT)

################# PILE LAYOUT #########################################

#   Define position of draw and discard piles, relative to oxygen
PILE_OFFSET = 340
PILE_02_OFFSET = -int(CARD_HEIGHT/2)
DRAW_PILE_POS = (int(PR_MX + PILE_OFFSET/2),
    int(OXYGEN_POS[1] - CARD_HEIGHT * 1.5 - PILE_02_OFFSET))
DISCARD_PILE_POS = (int(PR_MX - PILE_OFFSET/2 - CARD_WIDTH),
    int(OXYGEN_POS[1] - CARD_HEIGHT * 1.5 - PILE_02_OFFSET))

#   Command and to_discard
SECONDARY_VERTS = int(DRAW_PILE_POS[1] + CARD_HEIGHT*1.4)
COMMAND_PILE_POS = (DRAW_PILE_POS[0], SECONDARY_VERTS)
TO_DISCARD_POS = (DISCARD_PILE_POS[0], SECONDARY_VERTS)

#   Temporary pile for wormhole and salvage
TEMP_POS = (int(PR_MX - CARD_WIDTH/2), STAGE_POS[1] + CARD_HEIGHT)

################# SIDEBAR SETTINGS ####################################

SIDEBAR_WIDTH = WINDOW_WIDTH * 0.22
SIDEBAR_X_MARG = 20
SIDEBAR_Y_MARG = 50

LOG_WIDTH = SIDEBAR_WIDTH * 0.88
LOG_HEIGHT = WINDOW_HEIGHT * 0.20
LOG_XPOS = SIDEBAR_WIDTH * 0.06
LOG_YPOS = WINDOW_HEIGHT * 0.77

PREVIEW_MARGIN = 45

################# BUTTON SPACING ######################################

OPTION_ARRAY_WIDTH = LOG_WIDTH
OPTION_ARRAY_HEIGHT = WINDOW_HEIGHT*0.2
OPTION_ARRAY_DIMS = (OPTION_ARRAY_WIDTH, OPTION_ARRAY_HEIGHT)
SPACING_FROM_LOG = 15
OPTION_ARRAY_POS = (LOG_XPOS,
    int(LOG_YPOS - SPACING_FROM_LOG - OPTION_ARRAY_HEIGHT))

################# CARD ARRAY SETTINGS #################################

ARRAY_SPACING = 20

################# HAND SETTINGS #######################################

HAND_SCALE = 1.0
HAND_POS = (OXYGEN_POS[0], int(PR_BY - CARD_HEIGHT*HAND_SCALE/HAND_SCALE))

################# ANIMATION SETTINGS ##################################

#   Delay between animations, in seconds
ACTION_LENGTH = 0.85

################# FONTS ###############################################

CARDFONT = "None"
DECKFONT = "None"
PLAYERFONT = "None"
LOGFONT = "None"
BUTTONFONT = "None"
