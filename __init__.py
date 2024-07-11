# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction() -> None:
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo(f"total Card count: {cardCount}")

def testFunction2() -> None:
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    
    # show a message box
    showInfo(f"Total Card count: {cardCount}")

# create a new menu item, "test"
action = QAction("Test", mw)
action2 = QAction('Test all', mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
qconnect(action2.triggered, testFunction2)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
mw.form.menuTools.addAction(action2)


