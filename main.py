# import PyQt5 gui packages and built-in sys,time modules
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5 import QtGui, QtCore
import sys
import time

# import self-coded module under the same directory
from uiClass import *
from sqlTable import dbSetup

if __name__ == '__main__':

    dbSetup()  # create new database file to store user generated data (will skip on its own if db file already exists)

    # create application object and pass command-line arguments to the running scripts
    # served as a looping structure for mainWindow screen
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # setting application's looking style

    # create a custom SplashScreen object to be showed during application
    # loading time
    splash = QSplashScreen()
    img = QtGui.QPixmap('icons\\computer.png')
    splash.setPixmap(img)
    splash.show()
    time.sleep(1)  # delay 1s
    font = QtGui.QFont('Times', 24)
    splash.setFont(font)
    splash.showMessage("Tony Inc.", QtCore.Qt.AlignTop |
                       QtCore.Qt.AlignRight, QtCore.Qt.white)

    time.sleep(1)
    mainWindow = Window()  # create Window object imported from uiClass (main working module)
    mainWindow.show()
    # remove splashScreen object after mainWindow is loaded
    splash.finish(mainWindow)

    # sys.exit(app.exec()) instead of using app.exec_() directly to send the correct status code to the calling process
    # app.exec_() alone will send 0 even if application just crashed
    sys.exit(app.exec_())  # close the app when X is clicked
