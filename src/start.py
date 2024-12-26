import main
import ANSIEscapeSequences as ANSI
from typing import List

DEBUG = False
PLAYER = 0


def menu(text: List[str], color=ANSI.DEFAULT_COLOR, min_width=40) -> str:
    '''
    Draws a pretty little menu that automatically adjusts its size.

        text:   List of lines of text to be displayed

        color:  Font/Box color (default ANSI.DEFAULT_COLOR)

        min_width:  Minimum width of the menu (default 40)
    '''
    width = max(len(max(text, key = lambda x : len(x))), min_width)
    for i in range(len(text)):
        if (len(text[i]) < width):
            text[i] = " " * ((width - len(text[i]))//2) + text[i] + " " * ((width - len(text[i]))//2 + (width - len(text[i]))%2)

    print("┏" + "━" * (width * 2) + "┓")
    print("┃" + " " * (width * 2) + "┃")
    for line in text:
        print("┃" + " " * (width//2) + line + " " * (width//2 + width%2) + "┃ ")
        print("┃" + " " * (width * 2) + "┃")

    print("┗" + "━" * (width * 2) + "┛")


def main_menu():
    print(menu(["Welcome to terminal bomber!", "press ENTER to start"]))
    if input() == '':
        gamemode_menu()
    else:
        main_menu()


def gamemode_menu():
    global DEBUG
    print(menu(["(S) Single Player (kinda lame so far)", "(M) Multiplayer", "(D) Debug mode"]))
    inp = input()
    if inp == 'S' or inp == 's':
        DEBUG = True
        player_menu()
    elif inp == 'M' or inp == 'm':
        server_menu()
    elif inp == 'D' or inp =='d':
        DEBUG = True
        start()
    else:
        gamemode_menu()


def server_menu():
    global DEBUG
    print(menu(["(J) Join Room", "(H) Host Room"]))
    inp = input()
    if inp == 'J' or inp =='j':
        DEBUG = False
        player_menu()
    elif inp == 'H' or inp == 'h':
        DEBUG = False
        raise NotImplementedError("Yannis mach mal")
    else:
        server_menu()


def player_menu():
    global PLAYER
    print(menu(["(1) Player 1", "(2) Player 2", "... and so on"]))
    inp = input()
    try:
        int(inp)
    except ValueError:
        print("Not a number")
        player_menu()
    PLAYER = int(inp)
    main.start_game()


def start():
    main.DEBUG = DEBUG
    main.PLAYER = PLAYER
    main.start_game()


if __name__ == '__main__':
    main_menu()