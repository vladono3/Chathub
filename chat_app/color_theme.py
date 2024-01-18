THEME = "light"
CANVAS = "#1E2019"
BACKGROUND = "#1E2019"
BUTTON = "#587B7F"
HOVER = "#4d78cc"
TEXT = "#FFFFFF"


def change_theme(self):
    global THEME, CANVAS, BACKGROUND, BUTTON, HOVER, TEXT
    if THEME == "dark":
        THEME = "light"
        CANVAS = "#222831"
        BACKGROUND = "#222831"
        BUTTON = "#323844"
        HOVER = "#4d78cc"
        TEXT = "#FFFFFF"
    elif THEME == "light":
        THEME = "dark"
        CANVAS = "red"
        BACKGROUND = "yellow"
        BUTTON = "orange"
        HOVER = "white"
        TEXT = "#FFFFFF"
