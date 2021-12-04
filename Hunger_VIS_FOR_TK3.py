'''Missionaries3_VIS_FOR_TK3.py
Version of Sept. 17, 2019.
This visualization file works with Missionaries3.py and
Tk_SOLUZION_Client3.py.
It uses three jpg images for showing missionaries, cannibals, and the boat.

'''
from tkinter import font


myFont = None

WIDTH = 450
HEIGHT = 450
TITLE = 'Hunger Crisis Simulation'

STATE_WINDOW = None
STATE_ARRAY = None


def initialize_vis(st_win, state_arr, initial_state):
    global STATE_WINDOW, STATE_ARRAY
    STATE_WINDOW = st_win
    STATE_ARRAY = state_arr
    STATE_WINDOW.winfo_toplevel().title(TITLE)
    render_state(initial_state)


def render_state(s):
    # Note that font creation is only allowed after the Tk root has been
    # defined.  So we check here if the font creation is still needed,
    # and we do it (the first time this method is called).
    global myFont
    if not myFont:
        myFont = font.Font(family="Helvetica", size=18, weight="bold")
    #print("In render_state, state is "+str(s))
    # Create the default array of colors
    cyan = (0, 183, 235)
    orange = (255, 165, 0)
    red = (255, 0, 0)
    black = (0, 0, 0)

    row = [cyan] * 100
    the_color_array = [row]
    for i in range(99):
        the_color_array += [row[:]]
    # Now create the default array of string labels.
    row = ['' for i in range(100)]
    the_string_array = [row]
    for i in range(99):
        the_string_array += [row[:]]

    # Adjust colors and strings to match the state.

    row = 0
    col = 0

    for person in range(round(s.np / 100)):
        the_color_array[row][col] = cyan
        #the_color_array[row][col] = 'np.jpg'
        col = (col + 1) % 100
        if col == 0:
            row = (row + 1) % 100

    for person in range(round(s.mmp/100)):
        the_color_array[row][col] = orange
        # the_color_array[row][col] = 'mmp.jpg'
        col = (col + 1) % 100
        if col == 0:
            row = (row + 1) % 100

    for person in range(round(s.smp/100)):
        the_color_array[row][col] = red
        # the_color_array[row][col] = 'smp.jpg'
        col = (col + 1) % 100
        if col == 0:
            row = (row + 1) % 100

    for person in range(round(s.dead/100)):
        the_color_array[row][col] = black
        # the_color_array[row][col] = 'dead.jpg'
        col = (col + 1) % 100
        if col == 0:
            row = (row + 1) % 100

    #######

    caption = "Current state of the puzzle. Textual version: "+str(s)
    print(caption)
    the_state_array = STATE_ARRAY(color_array=the_color_array,
                                  string_array=the_string_array,
                                  text_font=myFont,
                                  caption=caption)
    #print("the_state_array is: "+str(the_state_array))
    the_state_array.show()


print("The Hunger VIS file has been imported.")
