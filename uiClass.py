# import necessary widgets under QtWidgets package in PyQt5
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QWidget,
    QStackedWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QToolBar,
    QAction,
    QRadioButton,
    QCalendarWidget,
    QTextEdit,
    QGridLayout,
    QLCDNumber,
    QTableView,
    QFrame,
    QFontDialog,
    QColorDialog,
    QGroupBox,
    QDateEdit,
    QDateTimeEdit,
    QStyleFactory)

# import QWebEngineView for the mini browser
from PyQt5.QtWebEngineWidgets import QWebEngineView
# import QSound class to play alarm ringtone
from PyQt5.QtMultimedia import QSound
# import QtCore and QtGui modules necessary for the program
from PyQt5 import QtCore, QtGui
# import QDatetTime class to deal with datetime within UI
from PyQt5.QtCore import QDateTime

# import PyQt5's database connector class and query class to deal with database that
# don't need to be represented in tablewidget
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


# import sqlite3 to deal with database in tablewidget
import sqlite3

# import datetime to check morning/evening/night for homePage background image
import datetime

# import dialog classes from self-coded dialogClass module to work with
# their respective parent widgets
from dialogClass import *

# declare a currentUserID as an empty string
# will be used as global variable
# an IMPORTANT data specifiers to query result from database for the
# current user
currentUserID = ""


# create a window class inherited from QMainWindow
# a main window class for MPPT to hold a stackedWidget that constitutes
# other major widgets
class Window(QMainWindow):

    # define constructor for Window class
    def __init__(self):

        # inherit existing attributes and methods within __init__ method of
        # QMainWindow class
        super().__init__()

        # setting up the Window's size, title and icon
        self.setGeometry(150, 80, 1600, 900)
        self.setWindowTitle("Multipurpose Personal Productivity Tool")
        self.setWindowIcon(QtGui.QIcon("icons\\computer1.png"))

        # declare a db attribute for a Window instance to create connection to
        # data.db file
        self.db = sqlite3.connect("data.db")
        # declare a c attribute for Window instance to act as the db's cursor
        # for SQL command execution (query)
        self.c = self.db.cursor()
        # set a counter to deal with alarm rings
        self.counter = 0
        # create a timer object in alarmCheck that calls alarmCheckData in every second to check if
        # an alarm's date and time is met or not
        self.alarmCheck()

        # create an object from QStackedWidget class as central_widget
        # create and add major widgets from the various inherited widget classes below into the central_widget
        # all the major widgets are being passed this Window class to act as
        # their parent window
        self.central_widget = QStackedWidget(self)
        self.signUpPage = SignUpMenu(self)
        self.loginPage = LoginMenu(self)
        self.homePage = Home(self)
        self.budgetTrackerPage = BudgetTracker(self)
        self.alarmPage = Alarm(self)
        self.calendarPage = Calendar(self)
        self.memoPage = Memo(self)
        self.browserPage = Browser(self)
        self.central_widget.addWidget(self.signUpPage)
        self.central_widget.addWidget(self.loginPage)
        self.central_widget.addWidget(self.homePage)
        self.central_widget.addWidget(self.budgetTrackerPage)
        self.central_widget.addWidget(self.alarmPage)
        self.central_widget.addWidget(self.calendarPage)
        self.central_widget.addWidget(self.memoPage)
        self.central_widget.addWidget(self.browserPage)
        self.central_widget.setCurrentWidget(self.loginPage)

        # finally, set Window's CentralWidget to central_widget to show them
        self.setCentralWidget(self.central_widget)

    # define a method for Window object to show it's toolbar
    # the toolbar contains acitonButtons with icons to navigate to their
    # respective major widgets page
    def windowToolbar(self):

        # create a QToolBar object and set as an attribute for the Window class
        self.toolbar = QToolBar()
        self.toolbar.setStyle(QStyleFactory.create("WindowsVista"))
        self.toolbar.setIconSize(QtCore.QSize(136, 136))
        self.toolbar.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon | QtCore.Qt.AlignLeading)
        self.addToolBar(QtCore.Qt.LeftToolBarArea,
                        self.toolbar)  # add toolbar to Window
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet('QToolBar{spacing:10px;}')

        # create 7 action buttons, each with its own function to call when they are being
        # actionButton.triggered.connect(go to certain page.... by changing
        # Window's centralWidget to certain major widget page)
        home = QAction(QtGui.QIcon("icons\\home.png"), "Home", self)
        home.setToolTip("Proceed to Home Page")
        home.triggered.connect(
            lambda: self.central_widget.setCurrentWidget(self.homePage))

        budget = QAction(QtGui.QIcon("icons\\budget.png"),
                         "Budget Tracker", self)
        budget.setToolTip("Proceed to Budget Tracker")
        budget.triggered.connect(
            lambda: self.central_widget.setCurrentWidget(self.budgetTrackerPage))

        alarm = QAction(QtGui.QIcon("icons\\alarm.png"), "Alarm", self)
        alarm.setToolTip("Proceed to Alarm")
        alarm.triggered.connect(
            lambda: self.central_widget.setCurrentWidget(self.alarmPage))

        calendarIcon = QAction(QtGui.QIcon(
            "icons\\calendar.png"), "Calendar", self)
        calendarIcon.setToolTip("Proceed to Calendar Page")
        calendarIcon.triggered.connect(
            lambda: self.central_widget.setCurrentWidget(self.calendarPage))

        memo = QAction(QtGui.QIcon("icons\\memo.png"), "Memo", self)
        memo.setToolTip("Proceed to Memo Page")
        memo.triggered.connect(
            lambda: self.central_widget.setCurrentWidget(self.memoPage))

        browser = QAction(QtGui.QIcon("icons\\browser.png"), "Browser", self)
        browser.setToolTip("Proceed to Mini Browser")
        browser.triggered.connect(
            lambda: self.central_widget.setCurrentWidget(self.browserPage))

        logout = QAction(QtGui.QIcon("icons\\logout.png"), "Logout", self)
        logout.setToolTip("Proceed to Logout")
        logout.triggered.connect(self.userLogout)

        actiongroups = [home, budget, alarm,
                        calendarIcon, memo, browser, logout]

        # add the list of action buttons into the toolbar and set fixed size
        # for them
        self.toolbar.addActions(actiongroups)
        for action in self.toolbar.actions():
            widget = self.toolbar.widgetForAction(action)
            widget.setFixedSize(136, 136)

    # alarmCheck method, have a timer object that will call alarmCheckData
    # every second to check the alarm
    def alarmCheck(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.alarmCheckData)
        timer.start(1000)  # start timer, specify it to refresh every 1s
        self.alarmCheckData()  # call alarmCheckData once the timer object is created

    # actual alarm checking method
    def alarmCheckData(self):

        # get current user's ID and today's date
        global currentUserID
        today = QDateTime.currentDateTime().toString("yyyy-MM-dd")
        today = f"{today}%"

        # if any user is logged in
        if currentUserID != "":

            # execute SQL command to find alarm in today's date with their time
            # to ring record for alarm checking
            with self.db:
                self.c.execute("SELECT datetime_,datetimeToRing,title,particular FROM AlarmTable \
                    WHERE userID = ? AND datetimeToRing LIKE ?", (currentUserID, today))

                # get evey query result and store into result variable
                result = self.c.fetchall()

            # if there is any alarm that met today's date
            if result:

                # get current date time for alrm comparison
                currentDateTime = QDateTime.currentDateTime()

                # compare the datetime record for each alarms in result with the current date time
                # sound the alarm with QSound object if the time is met (1
                # second accuracy)
                for alarm in result:
                    datetimeToRing = QDateTime.fromString(
                        alarm[1], "yyyy-MM-dd HH:mm:ss")
                    if currentDateTime.secsTo(datetimeToRing) > 0 and currentDateTime.secsTo(datetimeToRing) <= 1:
                        # create alarmRingDialog object from dialogClass
                        self.alarmDialog = alarmRingDialog(alarm, self)
                        self.alarmDialog.show()  # show the dialog
                        self.counter = 1  # counter add up

                        # if alarmRing dialog is not closed, keep play sound
                        if self.alarmDialog.closedState != True:
                            self.sound = QSound("alarmRingTone.wav")
                            self.sound.play()
                            self.sound.setLoops(-1)

        # if a user is logged in and the alarm is currently running
        if currentUserID != "" and self.counter == 1:

            # if the user closed the alarmRing dialog
            if self.alarmDialog.closedState == True:

                # reset the alarm counter to 0 and stop the ringtone
                self.counter = 0
                self.sound.stop()

    # userLogout method, reset every widgets' user data to default and set currentUserID back to empty string
    # return to login screen
    def userLogout(self):
        global currentUserID
        button = QMessageBox.question(
            self, "Logout", "Do you wish to logout?", QMessageBox.Yes | QMessageBox.Cancel)
        if button == QMessageBox.Yes:
            self.browserPage.browserInit()
            self.central_widget.removeWidget(self.homePage)
            self.homePage = Home(self)
            self.central_widget.insertWidget(2, self.homePage)
            self.budgetTrackerPage.resetTable()
            self.calendarPage.editor.setText("")
            self.alarmPage.resetTable()
            self.memoPage.resetTable()
            self.removeToolBar(self.toolbar)
            self.central_widget.setCurrentWidget(self.loginPage)
            QMessageBox.information(self, "Logout Success", f"{currentUserID} has been logged out!", QMessageBox.Ok)
            currentUserID = ""

# create SignUpMenu class inherited form QWdiget for sign up screen


class SignUpMenu(QWidget):

    # define constructor for SignUpMenu class
    def __init__(self, parent=None):

        # inherit existing __init__ method of QWidget class
        super(SignUpMenu, self).__init__(parent)

        # create necessary widgets
        self.fnameLabel = QLabel("First Name: ")
        self.fnameEdit = QLineEdit()
        self.fnameEdit.setPlaceholderText("Enter first name..")
        self.lnameLabel = QLabel("Last Name: ")
        self.lnameEdit = QLineEdit()
        self.lnameEdit.setPlaceholderText("Enter last name..")
        self.userGenderInput = QLabel("Gender: ")
        self.radioButtonMale = QRadioButton("Male")
        self.radioButtonFemale = QRadioButton("Female")
        self.userIdLabel = QLabel("User Id/Name: ")
        self.userIdSignUpEdit = QLineEdit()
        self.userIdSignUpEdit.setPlaceholderText("Enter User Id..")
        self.userPasswordLabel = QLabel("Password: ")
        self.userPasswordSignUpEdit = QLineEdit()
        self.userPasswordSignUpEdit.setPlaceholderText("Enter password..")
        self.userPasswordSignUpEdit.setEchoMode(QLineEdit.Password)
        self.userPasswordSignUpEdit.setMaxLength(10)
        self.userPasswordSignUpEdit.setToolTip("Maximum 10 characters!")
        self.backButton = QPushButton("Back to login")
        self.backButton.clicked.connect(self.goToLoginPage)
        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clearText)
        self.createAccountButton = QPushButton("Create Account")
        self.createAccountButton.clicked.connect(self.createAccount)

        self.signUpMenuUiSetup()  # call signUpMenu layout setup method

    # signUpMenu layout setup method
    def signUpMenuUiSetup(self):

        # create font1 for labels and font2 for lineEdit entries
        font1 = QtGui.QFont()
        font1.setPointSize(16)
        font2 = QtGui.QFont()
        font2.setPointSize(12)

        # assign specific size and fonts to the following created widgets
        for item in [self.fnameLabel, self.lnameLabel, self.userGenderInput, self.userIdLabel, self.userPasswordLabel]:
            item.setFixedSize(180, 40)
            item.setFont(font1)

        for item in [self.fnameEdit, self.lnameEdit, self.userIdSignUpEdit, self.userPasswordSignUpEdit]:
            item.setFixedSize(200, 40)
            item.setFont(font2)

        for item in [self.radioButtonFemale, self.radioButtonMale]:
            item.setFixedSize(90, 40)
            item.setStyleSheet("color: rgb(25,0,51)")
            item.setFont(font2)

        # actual layout setup starts here
        self.signUpformlayout = QVBoxLayout()
        self.mainHLayout = QHBoxLayout()
        self.hlayout1 = QHBoxLayout()
        self.hlayout1.addWidget(self.radioButtonMale)
        self.hlayout1.addWidget(self.radioButtonFemale)
        self.hlayout2 = QHBoxLayout()
        for button in [self.backButton, self.clearButton, self.createAccountButton]:
            self.hlayout2.addWidget(button)
        self.formLayout = QGridLayout()
        self.box = QGroupBox("User Sign Up Form")
        self.box.setStyle(QStyleFactory.create("Windows"))
        self.formLayout.addWidget(self.fnameLabel, 0, 0)
        self.formLayout.addWidget(self.fnameEdit, 0, 1)
        self.formLayout.addWidget(self.lnameLabel, 1, 0)
        self.formLayout.addWidget(self.lnameEdit, 1, 1)
        self.formLayout.addWidget(self.userGenderInput, 2, 0)
        self.formLayout.addLayout(self.hlayout1, 2, 1)
        self.formLayout.addWidget(self.userIdLabel, 3, 0)
        self.formLayout.addWidget(self.userIdSignUpEdit, 3, 1)
        self.formLayout.addWidget(self.userPasswordLabel, 4, 0)
        self.formLayout.addWidget(self.userPasswordSignUpEdit, 4, 1)
        self.formLayout.addLayout(self.hlayout2, 5, 0, 1, 1)

        self.box.setLayout(self.formLayout)

        self.mainHLayout.addStretch()
        self.mainHLayout.addWidget(self.box)
        self.mainHLayout.addStretch()
        self.signUpformlayout.addLayout(self.mainHLayout)
        self.signUpformlayout.setAlignment(QtCore.Qt.AlignCenter)

        # set SignUpMenu's layout to signUpformlayout
        self.setLayout(self.signUpformlayout)

    # a method to clear text in lineEdit entries, assigned to clear button's
    # clicked signal command
    def clearText(self):
        for item in [self.fnameEdit, self.lnameEdit, self.userIdSignUpEdit, self.userPasswordSignUpEdit]:
            item.setText("")

    # override QWidget's resizeEvent method to update SignUpMenu's background
    # image size with respect to the current window size
    def resizeEvent(self, event):
        loginBgImg = QtGui.QPixmap("icons\\smoke.jpg")
        loginBgImg = loginBgImg.scaled(self.parent().size(
        ), QtCore.Qt.KeepAspectRatioByExpanding, transformMode=QtCore.Qt.SmoothTransformation)
        self.setAutoFillBackground(True)
        self.palette = QtGui.QPalette()
        self.palette.setBrush(10, QtGui.QBrush(loginBgImg))
        self.setPalette(self.palette)

    # createAccound method, involves user input validation
    def createAccount(self):

        newUserFname = self.fnameEdit.text()
        newUserLname = self.lnameEdit.text()
        if self.radioButtonMale.isChecked():
            newUserGender = "Male"
        elif self.radioButtonFemale.isChecked():
            newUserGender = "Female"
        else:
            newUserGender = ""
        newUserId = self.userIdSignUpEdit.text()
        newUserPassword = self.userPasswordSignUpEdit.text()

        if newUserFname == "" or newUserLname == "" or newUserGender == "" or newUserId == "" or newUserPassword == "":
            QMessageBox.warning(self.parent().parent(
            ), "WARNING!", "You can't leave BLANK part in the form!", QMessageBox.Ok)

        # if every input widget is filled and not empty
        else:

            # create connection to database file and a QSqlQuery object to
            # execute SQL commands
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName('data.db')
            db.open()
            query = QSqlQuery()

            # first way to run SQL command using QSqlQuery object, %string formatting is used
            # to create a string of SQL command
            sql = "SELECT * FROM UserTable WHERE userID = '%s'" % (newUserId)
            query.exec_(sql)  # execute SQL command

            # check if the userID existed or not, if it does, the inputs will
            # be cleared and a warning messagebox will pop up
            if query.next():
                QMessageBox.warning(self.parent().parent(), "WARNING!", f"The User ID: {newUserId} already exist! Please enter new ID.", QMessageBox.Ok)
                self.clearText()

            # if userID is new and not in database
            else:
                # second way to run SQL command in QSqlQuery object, .prepare method will receive SQL string with '?' placeholders
                # .addBindValue will pass values into the respective '?' in the .prepare() SQL command
                query.prepare("INSERT INTO UserTable(userFirstName, userLastName, userID, userPassword, userGender) "
                              "VALUES (?,?,?,?,?)")
                query.addBindValue(newUserFname)
                query.addBindValue(newUserLname)
                query.addBindValue(newUserId)
                query.addBindValue(newUserPassword)
                query.addBindValue(newUserGender)

                # if the SQL command runs successfully:
                if query.exec_():
                    db.commit()  # QSqlDatabase object commit to update changes
                    QMessageBox.information(self.parent().parent(), "Take Note", f"{newUserId}'s account successfully created! You may now Login.", QMessageBox.Ok)
                    self.goToLoginPage()  # go to login page

            db.close()  # close db's connection to data.db
            self.clearText()  # clear text in entries

    # goToLogin, set Window's central widget's current widget to loginPage
    def goToLoginPage(self):
        self.parent().setCurrentWidget(self.parent().parent().loginPage)
        self.clearText()

# inherit QWidget for LoginMenu class


class LoginMenu(QWidget):

    # define constructor for LoginMenu class
    def __init__(self, parent=None):
        # retain parent's __init__ function's attributes and methods
        super(LoginMenu, self).__init__(parent)

        # create necessary widgets
        self.userIdLabel = QLabel("User Id")
        self.userIdLoginEdit = QLineEdit()
        self.userIdLoginEdit.setPlaceholderText("Enter User Id..")
        self.userPasswordLabel = QLabel("Password")
        self.userPasswordLoginEdit = QLineEdit()
        self.userPasswordLoginEdit.setMaxLength(10)
        self.userPasswordLoginEdit.setToolTip("Maximum 10 characters!")
        self.userPasswordLoginEdit.setPlaceholderText("Enter Password..")
        self.userPasswordLoginEdit.setEchoMode(QLineEdit.Password)

        # create 3 buttons and assign them with a specific function to call
        # when being clicked
        self.signUpButton = QPushButton("Sign Up")
        self.signUpButton.clicked.connect(self.goToSignUpPage)
        self.loginButton = QPushButton("Log In")
        self.loginButton.clicked.connect(self.accountLogin)
        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clearText)

        self.loginMenuUiSetup()  # call the loginMenu layout setup method

    # loginMenu layout setup method
    def loginMenuUiSetup(self):

        # create fonts and layouts
        font1 = QtGui.QFont()
        font1.setPointSize(16)
        font2 = QtGui.QFont()
        font2.setPointSize(12)
        self.loginformlayout = QGridLayout()
        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()
        self.hlayout3 = QHBoxLayout()

        # set size and fonts of the following widgets
        # set the button's stylsesheet for text to appear as "shifting" when
        # being clicked, color khaki is used
        for item in [self.userIdLabel, self.userPasswordLabel]:
            item.setFixedSize(150, 40)
            item.setFont(font1)
        for item in [self.userIdLoginEdit, self.userPasswordLoginEdit]:
            item.setFixedSize(200, 40)
            item.setFont(font2)
        for item in [self.clearButton, self.signUpButton, self.loginButton]:
            item.setFont(font2)
            item.setStyleSheet("""QPushButton:hover {
                            background-color: khaki;}
                            QPushButton:pressed {
                            padding-left: 5px;
                            padding-top: 5px;
                            background-color: #d0d67c;}""")
            self.hlayout3.addWidget(item)

        self.loginformlayout.setColumnStretch(0, 1)
        self.loginformlayout.setColumnStretch(3, 1)
        self.loginformlayout.setRowStretch(0, 1)
        self.loginformlayout.setRowStretch(4, 1)
        self.hlayout1.addWidget(self.userIdLabel)
        self.hlayout1.addWidget(self.userIdLoginEdit)
        self.hlayout2.addWidget(self.userPasswordLabel)
        self.hlayout2.addWidget(self.userPasswordLoginEdit)
        self.loginformlayout.addLayout(self.hlayout1, 1, 1)
        self.loginformlayout.addLayout(self.hlayout2, 2, 1)
        self.loginformlayout.addLayout(self.hlayout3, 3, 1)

        # set loginMenu's layout to loginformlayout
        self.setLayout(self.loginformlayout)

    # resize event, same as the signUpMenu's description, deal with background
    # image resizing
    def resizeEvent(self, event):
        loginBgImg = QtGui.QPixmap("icons\\login.png")
        loginBgImg = loginBgImg.scaled(self.parent().size(
        ), QtCore.Qt.KeepAspectRatioByExpanding, transformMode=QtCore.Qt.SmoothTransformation)
        self.setAutoFillBackground(True)
        self.palette = QtGui.QPalette()
        self.palette.setBrush(10, QtGui.QBrush(loginBgImg))
        self.setPalette(self.palette)

    # clear text in entries
    def clearText(self):
        self.userIdLoginEdit.setText("")
        self.userPasswordLoginEdit.setText("")

    # go to signUpPage by setting Window's central_widget's current widget to
    # signUpPage
    def goToSignUpPage(self):
        self.parent().setCurrentWidget(self.parent().parent().signUpPage)

    # a method to login user
    # include user input validation
    def accountLogin(self):
        loginUserID = self.userIdLoginEdit.text()
        loginUserPassword = self.userPasswordLoginEdit.text()

        if loginUserID == "" or loginUserPassword == "":
            QMessageBox.critical(self.parent().parent(
            ), "Login Error", "Do not leave login form as BLANK!", QMessageBox.Ok)

        # if input is valid
        else:
            # run SQL command to check if user exists or not
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName('data.db')
            db.open()
            query = QSqlQuery()

            sql = "SELECT * FROM UserTable WHERE userID = '%s'" % (loginUserID)
            query.exec_(sql)

            # if there is no result from the query, means user doesn't exist
            if not query.next():
                QMessageBox.warning(self.parent().parent(
                ), "Login Error", "The User ID entered does NOT exist!", QMessageBox.Ok)

            else:
                # if exist, check if userID and userPassword is correct with
                # the data in UserTable from database file
                if loginUserID == query.value(2) and loginUserPassword == query.value(3):
                    global currentUserID
                    currentUserID = loginUserID  # UPDATE currentUserID to the login's userId
                    self.goToHomePage()
                else:
                    QMessageBox.warning(self.parent().parent(
                    ), "Login Error", "Password does not match!", QMessageBox.Ok)
            self.clearText()
            db.close()  # close database connection

    # go to homePage of MPPT, access and call Window's windowToolbar method to
    # create toolbar for page navigation
    def goToHomePage(self):
        self.parent().parent().windowToolbar()
        self.parent().parent().homePage.homeUiSetup()
        self.parent().setCurrentWidget(self.parent().parent().homePage)

    # update the keyPressEvent inherited from QWidget class
    # for every keystroke event, if key is equals to ENTER or Return,
    # proceed to accoundLogin() function if the entries have focus (clicked
    # and active, means user just typed in the entry)
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Enter or QKeyEvent.key() == QtCore.Qt.Key_Return:
            if self.userPasswordLoginEdit.hasFocus() or self.userIdLoginEdit.hasFocus():
                self.accountLogin()

# inherit QWidget class for Home class


class Home(QWidget):

    # define Home class' constructor
    def __init__(self, parent=None):
        # retain QWidget class' __init__ method's attributes and methods
        super(Home, self).__init__(parent)
        # set enable background filling, was used in LoginMenu and SignUpMenu
        self.setAutoFillBackground(True)

        # call chooseImg method
        self.chooseImg()

        # create database connection with data.db and create a cursor object to
        # execute SQL command
        self.db = sqlite3.connect('data.db')
        self.c = self.db.cursor()

    # Home's layout setup method
    def homeUiSetup(self):
        global currentUserID  # get currentUserID

        # using context manager to work with database
        with self.db:
            self.c.execute(
                "SELECT userLastName, userGender FROM UserTable WHERE userID =?", (currentUserID,))
            result = self.c.fetchone()  # get result after cursor executed SQL command

        # give title to the user, to be displayed in home page
        title = "Mr." if result[1] == "Male" else "Ms."
        userHonorificsName = f"{title} {result[0]}"  # eg. Mr. Lee

        # create fonts
        font1 = QtGui.QFont("Arial", 32)
        font2 = QtGui.QFont("Arial", 36)

        # create a custom DigtalClock class object
        self.clock = DigitalClock(self)
        self.greeting = QLabel("Welcome back,")
        self.greeting.setFont(font1)
        self.greeting.setStyleSheet("color: white")
        self.userName = QLabel(userHonorificsName)
        self.userName.setFont(font2)
        self.userName.setStyleSheet("color: white")

        # display current date as eg. Monday, 1 June
        self.date = QLabel(
            QDateTime.currentDateTime().toString("dddd, d MMMM"))
        self.date.setFont(font1)
        self.date.setStyleSheet("color: white")

        self.grid = QGridLayout()
        self.grid.setColumnStretch(0, 1)
        self.grid.setRowStretch(1, 1)
        self.grid.addWidget(self.greeting, 0, 0)
        self.grid.addWidget(self.userName, 1, 0, QtCore.Qt.AlignTop)
        self.grid.addWidget(self.clock, 3, 4, QtCore.Qt.AlignRight)
        self.grid.addWidget(
            self.date, 4, 4, QtCore.Qt.AlignLeft | QtCore.Qt.AlignHCenter)
        self.setLayout(self.grid)  # set Home layout

    # choose Home's background image based on current time
    # the three images are for morning,evening and night
    def chooseImg(self):
        dt = datetime.datetime.now()
        if dt.time() <= datetime.time(14):
            self.fileName = "morning.jpg"
        elif dt.time() > datetime.time(14) and dt.time() < datetime.time(19):
            self.fileName = "evening.jpg"
        elif datetime.time(19) <= dt.time() or dt.time() < datetime.time(5):
            self.fileName = "night.jpg"

    # background image resizer, same as SignUpMenu & LoginMenu
    def resizeEvent(self, event):
        self.Img = QtGui.QPixmap(f"icons\\{self.fileName}")
        self.Img = self.Img.scaled(self.size(
        ), QtCore.Qt.KeepAspectRatioByExpanding, transformMode=QtCore.Qt.SmoothTransformation)
        self.setAutoFillBackground(True)
        self.palette = QtGui.QPalette()
        self.palette.setBrush(10, QtGui.QBrush(self.Img))
        self.setPalette(self.palette)

# create a BudgetTracker widget inherited from QWidget class


class BudgetTracker(QWidget):

    # define a constructor for BudgetTracker widget
    def __init__(self, parent=None):
        # retain QWidget's default __ini__ constructor
        super(BudgetTracker, self).__init__(parent)

        # establish database connection and create a cursor object to execute
        # SQL command
        self.db = sqlite3.connect("data.db")
        self.c = self.db.cursor()

        # create necessary widgets
        # each buttons is assigned with a method to call when being clicked
        self.dateEditLabel = QLabel("Year and Month selection: ")
        self.dateEdit = QDateEdit()
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        self.dateEdit.setDisplayFormat("yyyy-MM")
        self.dateEdit.setFixedWidth(200)
        self.okButton = QPushButton("LOAD")
        self.okButton.clicked.connect(self.groupBoxAllowed)
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.addRow)
        self.editButton = QPushButton("Edit")
        self.editButton.clicked.connect(self.editRow)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.removeRow)
        self.endingBalButton = QPushButton("Calculate Ending Balance")
        self.endingBalButton.clicked.connect(self.calculateEndBal)
        self.endBalLabel = QLabel("Ending Balance: ")
        self.endBalRM = QLabel("RM")
        font = QtGui.QFont("Times", 20)
        self.endBalRM.setFont(font)
        self.endBalRM.setAlignment(QtCore.Qt.AlignRight)

        # create a QLCDNumber object to display numbers
        self.endBalLCD = QLCDNumber(self)
        self.endBalLCD.setSegmentStyle(QLCDNumber.Flat)
        self.endBalLCD.setDigitCount(12)
        self.endBalLCD.setMaximumHeight(50)
        self.endBalLCD.setMinimumHeight(40)
        self.endBalLCD.setStyleSheet("color: black")

        self.tableInitialSetup()  # initiate debit and credit tables
        self.budgetUiSetup()  # call the layout setup method of BudgetTracker class
        self.groupBoxInit()  # initiate groupBoxes within budgetTracker layout

    # define budgetTracker's layout setup
    def budgetUiSetup(self):
        self.mainVLayout = QVBoxLayout()
        self.mainHLayout1 = QHBoxLayout()
        self.mainHLayout2 = QHBoxLayout()
        self.debitTableLayout = QHBoxLayout()
        self.creditTableLayout = QHBoxLayout()
        self.buttonVLayout = QVBoxLayout()
        self.miniHlayout = QHBoxLayout()

        self.box1 = QGroupBox("Selection: ")
        self.box2 = QGroupBox("Debit Table")
        self.box3 = QGroupBox("Credit Table")
        self.box4 = QGroupBox("Action Buttons")

        self.mainHLayout1.addWidget(self.dateEditLabel)
        self.mainHLayout1.addWidget(self.dateEdit)
        self.mainHLayout1.addStretch(1)
        self.mainHLayout1.addWidget(self.okButton)
        self.box1.setLayout(self.mainHLayout1)
        self.debitTableLayout.addWidget(self.debitTable)
        self.box2.setLayout(self.debitTableLayout)
        self.creditTableLayout.addWidget(self.creditTable)
        self.box3.setLayout(self.creditTableLayout)

        # set fonts and height for buttons
        font = QtGui.QFont("Times", 12)
        for button in [self.addButton, self.editButton, self.deleteButton, self.endingBalButton]:
            button.setMaximumHeight(120)
            button.setFont(font)
            self.buttonVLayout.addWidget(button)

        self.buttonVLayout.addStretch()
        self.buttonVLayout.addWidget(self.endBalLabel)
        self.miniHlayout.addWidget(self.endBalRM)
        self.miniHlayout.addWidget(self.endBalLCD)
        self.buttonVLayout.addLayout(self.miniHlayout)

        self.box4.setLayout(self.buttonVLayout)

        for box in [self.box2, self.box3, self.box4]:
            self.mainHLayout2.addWidget(box)

        self.mainVLayout.addWidget(self.box1)
        self.mainVLayout.addLayout(self.mainHLayout2)
        # set budgetTracker's layout to mainVLayout
        self.setLayout(self.mainVLayout)

    # table setup method
    # create 2 tables, namely debit and credit table
    def tableInitialSetup(self):
        self.debitTable = QTableWidget()
        self.creditTable = QTableWidget()

        # table formatting for both tables
        for table in [self.debitTable, self.creditTable]:
            table.setEditTriggers(QTableView.NoEditTriggers)
            table.setAlternatingRowColors(True)
            table.setSelectionMode(QTableView.SingleSelection)
            table.setSelectionBehavior(QTableView.SelectRows)
            table.setRowCount(0)
            table.setColumnCount(7)
            table.setHorizontalHeaderLabels(
                ["User", "yearMonth", "Type", "Date", "Particulars", "Reference", "Amount(RM)"])

            # hide columns 0,1,2 where user don't have to interact with them
            table.hideColumn(0)
            table.hideColumn(1)
            table.hideColumn(2)
            table.horizontalHeader().setStretchLastSection(True)
            table.resizeColumnsToContents()
            table.resizeRowsToContents()

    # populate table method
    def populateTable(self):
        # turn stretchLastSection to false before adding data
        for table in [self.debitTable, self.creditTable]:
            table.horizontalHeader().setStretchLastSection(False)

        global currentUserID  # get currentUserID

        # get selected year and month in string from the budgetTracker's
        # dateEdit user input
        yearMonth = self.dateEdit.dateTime()
        yearMonth = yearMonth.toString("yyyy-MM")

        # search for budgetRecords of the current user in BudgetRecordTable
        with self.db:
            self.c.execute(
                "SELECT * FROM BudgetRecordTable WHERE userID = ? AND yearMonth_ = ? AND type = 'debit'", (currentUserID, yearMonth))
            # result will accept all data in BudgetRecordTable of the query
            # result
            result = self.c.fetchall()

            # set new row count of debit table according to number of rows in
            # query result
            self.debitTable.setRowCount(len(result))

            # use for loops to populate debit table with row and columns
            for row, row_data in enumerate(result):
                for col, data in enumerate(row_data):
                    newData = QTableWidgetItem(data)
                    newData.setToolTip(f"{data}")
                    self.debitTable.setItem(row, col, newData)

        # do the same thing for credit table
        with self.db:
            self.c.execute(
                "SELECT * FROM BudgetRecordTable WHERE userID = ? AND yearMonth_ = ? AND type = 'credit'", (currentUserID, yearMonth))
            result = self.c.fetchall()

            self.creditTable.setRowCount(len(result))

            for row, row_data in enumerate(result):
                for col, data in enumerate(row_data):
                    newData = QTableWidgetItem(data)
                    newData.setToolTip(f"{data}")
                    self.creditTable.setItem(row, col, newData)

        # reformat both tables according to contents' size after being
        # populated
        for table in [self.debitTable, self.creditTable]:
            table.resizeColumnsToContents()
            table.resizeRowsToContents()
            table.horizontalHeader().setStretchLastSection(True)

    # initialize boxes in layout, set their check states
    def groupBoxInit(self):
        for box in [self.box2, self.box3]:
            box.setFlat(True)
            box.setCheckable(False)
            box.setChecked(False)

    # allow groupbox to be checked once user clicked "load" or okButton
    # populate table
    def groupBoxAllowed(self):
        self.box2.setCheckable(True)
        self.box3.setCheckable(True)
        self.box2.setChecked(True)
        self.box3.setChecked(False)
        self.populateTable()

    # reset credit and debit table when a user is loged out
    # reset the check states of the boxes
    def resetTable(self):
        for table in [self.debitTable, self.creditTable]:
            table.setRowCount(0)
            table.setColumnCount(7)

        for box in [self.box2, self.box3]:
            box.setChecked(False)

    # method to check if which table is being selected (its groupBox is found to be checked)
    # return respective table objects or None if none is chosed
    def selectedTable(self):
        if self.box2.isChecked() and self.box3.isChecked() != True:
            return self.debitTable
        elif self.box3.isChecked() and self.box2.isChecked() != True:
            return self.creditTable
        else:
            return None

    # add a new row of budget record
    def addRow(self):

        # check which table is being checked (their box)
        table = self.selectedTable()

        # if no box is checked
        if table == None:
            QMessageBox.warning(self, "Table selection error",
                                "Please check on AT LEAST ONE and ONLY ONE Table to add records!", QMessageBox.Ok)
        else:
            # get currentUserID and year month detail from BudgetTracker's
            # dateEdit
            global currentUserID
            yearMonth = self.dateEdit.dateTime()
            yearMonth = yearMonth.toString("yyyy-MM")

            # instantiate a custom inputBudgetDialog(imported from dialogClass) object
            # pass selected table object and yearMonth details to the dialog
            self.inputDialog = inputBudgetDialog(table, yearMonth, self)
            self.inputDialog.exec_()  # execute dialog

            # if action is done in the dialog window
            if self.inputDialog.state:

                # get details from various widgets in the dialog
                dataType = self.inputDialog.dataType.text()
                date_ = self.inputDialog.dateEdit.dateTime()
                date_ = date_.toString("yyyy-MM-dd")
                particular = self.inputDialog.particularEdit.text()
                reference = self.inputDialog.referenceEdit.text()
                amount = self.inputDialog.amountEdit.value()
                amount = f"{amount:.2f}"
                # create a dataList to be used in SQL command
                dataList = [currentUserID, yearMonth, dataType,
                            date_, particular, reference, amount]

                # insert new row of data into BudgetRecordTable with values in
                # dataList
                with self.db:
                    self.c.execute(
                        "INSERT INTO BudgetRecordTable VALUES(?,?,?,?,?,?,?)", tuple(dataList))
                self.populateTable()  # populate and update table

    # edit a row
    def editRow(self):

        # get selected table
        table = self.selectedTable()

        if table == None:
            QMessageBox.warning(self, "Table Selection Error",
                                "Please check on AT LEAST ONE and ONLY ONE Table for record to be edited", QMessageBox.Ok)

        else:
            row = table.currentRow()  # get current row in a table

            # if no row is selected..
            if row == -1:
                QMessageBox.warning(self, "Record Selection Error",
                                    "Please select a row of budget record to be deleted!", QMessageBox.Ok)

            else:
                # get currentUserID and yearmonth detail from dateEdit
                global currentUserID
                yearMonth = self.dateEdit.dateTime().toString("yyyy-MM")
                dataType = "debit" if table == self.debitTable else "credit"

                # get items' text in the selected row and create a datalist to
                # be used in SQL command
                date_ = table.item(row, 3).text()
                particular = table.item(row, 4).text()
                reference = table.item(row, 5).text()
                amount = table.item(row, 6).text()

                # the data list
                dataToEdit = (currentUserID, yearMonth, dataType,
                              date_, particular, reference, amount)

                # look for the query result
                with self.db:

                    self.c.execute("SELECT * FROM BudgetRecordTable WHERE userID = ? AND yearMonth_ = ? AND type = ? AND date_ = ?\
                        AND particular = ? AND reference = ? AND amount = ?", dataToEdit)

                    result = self.c.fetchone()

                # create a custom editBudgetDialog object(imported from dialogClass)
                # pass the result list into the dialog
                self.editDialog = editBudgetDialog(result, self)
                self.editDialog.exec_()  # execute the dialog window

                # if action is done..
                if self.editDialog.state:

                    # get details from various widgets in the editDialog window
                    yearMonth_ = self.editDialog.yearMonthEdit.dateTime().toString("yyyy-MM")
                    dataType = self.editDialog.dataType.currentText()
                    date_ = self.editDialog.dateEdit.dateTime().toString("yyyy-MM-dd")
                    particular = self.editDialog.particularEdit.text()
                    reference = self.editDialog.referenceEdit.text()
                    amount = self.editDialog.amountEdit.value()
                    amount = f"{amount:.2f}"

                    # put the details into a tuple and add the query result to
                    # be used in SQL command
                    dataList = (yearMonth_, dataType, date_,
                                particular, reference, amount)
                    dataList += result

                    # update the BudgetRecordTable for the row which meets the
                    # searching requirement (WHERE...)
                    with self.db:

                        self.c.execute("UPDATE BudgetRecordTable SET yearMonth_ = ?, type = ?, date_ = ?, particular = ?,\
                            reference = ?, amount = ? WHERE userID = ? AND yearMonth_ = ? AND type = ? AND date_ = ?\
                            AND particular = ? AND reference =? AND amount = ?", dataList)

                    self.populateTable()  # populate and update the table

    # remove a row
    def removeRow(self):
        # get selected table
        table = self.selectedTable()

        if table == None:
            QMessageBox.warning(self, "Table Selection Error",
                                "Please check on AT LEAST ONE and ONLY ONE Table for record to be removed", QMessageBox.Ok)
        else:
            row = table.currentRow()  # get current row

            # if no row is selected...
            if row == -1:
                QMessageBox.warning(self, "Record Selection Error",
                                    "Please select a row of budget record to be deleted!", QMessageBox.Ok)

            else:
                choice = QMessageBox.question(
                    self, "Remove Budget Record", "Are you certain that you want to remove this selected record?", QMessageBox.Yes | QMessageBox.No)

                # if user confirms deletion...
                if choice == QMessageBox.Yes:

                    # get currentUserID and year month details from dateEdit
                    global currentUserID
                    yearMonth = self.dateEdit.dateTime()
                    yearMonth = yearMonth.toString("yyyy-MM")
                    dataType = "debit" if table == self.debitTable else "credit"

                    # get the item details from the selected row
                    date_ = table.item(row, 3).text()
                    particular = table.item(row, 4).text()
                    reference = table.item(row, 5).text()
                    amount = table.item(row, 6).text()

                    # add the details into a tuple to be used in SQL command
                    dataRemove = (currentUserID, yearMonth, dataType,
                                  date_, particular, reference, amount)

                    # delete a row of data from BudgetRecordTable which meets
                    # the requirement (WHERE...)
                    with self.db:
                        self.c.execute("DELETE FROM BudgetRecordTable WHERE userID = ? AND yearMonth_ = ?\
                            AND type = ? AND date_  = ? AND particular = ? AND reference = ? AND amount = ?", dataRemove)

                    self.populateTable()  # populate and update table
                    QMessageBox.information(
                        self, "Remove Budget Record", "Budget record successfully removed!", QMessageBox.Ok)

    # calculate ending balance, called once "calc end bal"button is clicked
    def calculateEndBal(self):

        # make sure at least one table is checked (indicate that budget record
        # is loaded)
        table = self.selectedTable()
        if table == None:
            QMessageBox.warning(self, "Record Selection Error",
                                "Please click the LOAD button to load budget record on specific Month and Year!")
        else:

            # get currentUserID and year month details
            global currentUserID
            yearMonth = self.dateEdit.dateTime().toString("yyyy-MM")

            # create tuple to query debit data and credit data
            queryDebitData = (currentUserID, yearMonth, "debit")
            queryCreditData = (currentUserID, yearMonth, "credit")

            # create 2 empty list of debit and credit's total
            debitTotal = []
            creditTotal = []

            # query for the amount of all row of data in BudgetRecordTable
            # where type is'debit' and...
            with self.db:
                self.c.execute("SELECT amount FROM BudgetRecordTable WHERE userID = ? AND\
                    yearMonth_ = ? AND type = ?", queryDebitData)

                result = self.c.fetchall()

                # reassign a new list to debitTotal where each element is a
                # float(amount) from query result
                debitTotal = [float(num[0]) for num in result]

            # do the same thing for creditTotal
            with self.db:
                self.c.execute("SELECT amount FROM BudgetRecordTable WHERE userID = ? AND\
                    yearMonth_ = ? and type = ?", queryCreditData)

                result = self.c.fetchall()

                creditTotal = [float(num[0]) for num in result]

            # calculate endBalance
            # endBal will return 0 if no items in debitTotal & creditTotal
            endBalance = float(sum(debitTotal) - sum(creditTotal))

            # set text of endBalLabel according to the yearMonth
            self.endBalLabel.setText(f"Ending balance for {yearMonth}: ")

            # create a string variable of endBalance with 2 decimal places
            # passed to endBalLCD to be displayed
            textToDisplay = f"{endBalance:.2f}"
            self.endBalLCD.display(textToDisplay)

# create an Alarm widget inherited from QWidget


class Alarm(QWidget):

    # define constructor for Alarm class
    def __init__(self, parent=None):
        super(Alarm, self).__init__(parent)

        # establish connection to data.db database file and a cursor object to
        # execute SQL command
        self.db = sqlite3.connect("data.db")
        self.c = self.db.cursor()

        # create table
        self.listTable = QTableWidget()
        self.listTable.setShowGrid(False)
        self.listTable.setEditTriggers(QTableView.NoEditTriggers)
        self.listTable.setAlternatingRowColors(True)
        self.listTable.setSelectionMode(QTableView.SingleSelection)
        self.listTable.setSelectionBehavior(QTableView.SelectRows)
        self.listTable.horizontalHeader().setStretchLastSection(True)
        self.listTable.setRowCount(0)
        self.listTable.setColumnCount(5)
        self.listTable.setHorizontalHeaderLabels(
            ["User", "Date and Time", "Date & Time to Ring", "Alarm Title", "Alarm Particulars"])
        # hide column 0 which display User, user don't have to work with that
        self.listTable.hideColumn(0)

        # create buttons and assign them with different methods
        self.loadButton = QPushButton("LOAD ALARM")
        self.loadButton.clicked.connect(self.populateTable)
        self.addButton = QPushButton("ADD")
        self.addButton.clicked.connect(self.addRow)
        self.editButton = QPushButton("EDIT")
        self.editButton.clicked.connect(self.editRow)
        self.removeButton = QPushButton("REMOVE")
        self.removeButton.clicked.connect(self.removeRow)

        self.alarmUiSetup()  # call the layout setup method for Alarm widget

    # reset the table when a user is logged out by resetting column and row
    # counts
    def resetTable(self):
        self.listTable.setRowCount(0)
        self.listTable.setColumnCount(5)

    # alarm layout setup method
    def alarmUiSetup(self):

        self.mainHLayout = QHBoxLayout()
        self.smallHLayout = QHBoxLayout()
        self.verticalLayout = QVBoxLayout()
        self.group1 = QGroupBox("Alarm Section")
        self.group2 = QGroupBox("Action Buttons")

        font = QtGui.QFont()
        font.setPointSize(12)

        # set fonts and stylesheet of buttons
        for item in [self.loadButton, self.addButton, self.editButton, self.removeButton]:
            item.setFont(font)
            item.setStyleSheet("color: green")
            self.verticalLayout.addWidget(item)

        self.group2.setLayout(self.verticalLayout)
        self.smallHLayout.addWidget(self.listTable)
        self.group1.setLayout(self.smallHLayout)
        self.mainHLayout.addWidget(self.group1)
        self.mainHLayout.addWidget(self.group2)
        self.setLayout(self.mainHLayout)  # set Alarm's layout to mainHLayout

    # populateTable method fills table with query result of current user
    def populateTable(self):

        # get currentuserID
        global currentUserID
        self.listTable.horizontalHeader().setStretchLastSection(False)

        # get currentUser's alarmData from the AlarmTable in database file
        with self.db:
            self.c.execute("SELECT * FROM AlarmTable WHERE userID = ?",
                           (currentUserID,))
            alarmData = self.c.fetchall()

            # set table's row according to rows in query result
            self.listTable.setRowCount(len(alarmData))

            # use for loop to fill up table using data from alarmData in a row
            # and column manner
            for row, row_data in enumerate(alarmData):
                for col, data in enumerate(row_data):
                    newData = QTableWidgetItem(data)
                    newData.setToolTip(f"{data}")
                    self.listTable.setItem(
                        row, col, newData)  # setItem to table

        self.listTable.resizeColumnsToContents()
        self.listTable.horizontalHeader().setStretchLastSection(True)
        self.listTable.resizeRowsToContents()

    # add a new row
    def addRow(self):
        global currentUserID

        # create an custom inputAlarmDialog (imported from dialogClass) object
        self.inputDialog = inputAlarmDialog(self)
        self.inputDialog.exec_()  # execute dialog window

        # if action is done in the dialog
        if self.inputDialog.state:

            # get data from the dialog's widgets
            dateTimeDetail = self.inputDialog.dateTimeEdit.dateTime()
            dateTime_ = dateTimeDetail.toString("yyyy-MM-dd HH:mm:ss")
            dateTimeTRDetail = self.inputDialog.dateTimeTREdit.dateTime()
            dateTimeTR = dateTimeTRDetail.toString("yyyy-MM-dd HH:mm:ss")
            alarmTitle = self.inputDialog.alarmTitleEdit.text()
            alarmDetail = self.inputDialog.alarmDetailEdit.toPlainText()

            # create a list of data to be inserted into the AlarmTable
            dataList = [currentUserID, dateTime_,
                        dateTimeTR, alarmTitle, alarmDetail]

            # insert the new data into new row of the AlarmTable
            with self.db:
                self.c.execute("INSERT INTO AlarmTable VALUES (?,?,?,?,?)",
                               tuple(dataList))

            self.populateTable()  # call populateTabke() to update the table view

    # edit a row
    def editRow(self):

        global currentUserID

        # get current selected row in the table
        row = self.listTable.currentRow()

        # warns user if no row is selected
        if row == -1:
            QMessageBox.warning(self, "Action Error",
                                "Please SELECT a ROW!", QMessageBox.Ok)
        else:

            # get dateTime from the selected row to be used in SQL commands
            dateTime_Item = self.listTable.item(row, 1)
            dateTime_ = dateTime_Item.text()

            # get the row data from the database based on currentUserID and the
            # selcted dateTime
            with self.db:
                self.c.execute("SELECT datetime_,datetimeToRing,title,particular FROM AlarmTable WHERE userID = ? AND datetime_ = ?",
                               (currentUserID, dateTime_))
                result = self.c.fetchone()

            # instantiate a custom editAlarmDialog (imported from dialogCLass) and pass the query result into it
            # to be displayed on respective widgets in the dialog window
            self.editDialog = editAlarmDialog(
                result[0], result[1], result[2], result[3], self)
            self.editDialog.exec_()  # execute the dialog Window

            # if action is done by user
            if self.editDialog.state:

                # get details from each widget and store them in a dataList for
                # SQL command
                dateTimeDetail = self.editDialog.dateTimeEdit.dateTime()
                dateTime_ = dateTimeDetail.toString("yyyy-MM-dd HH:mm:ss")
                dateTimeTRDetail = self.editDialog.dateTimeTREdit.dateTime()
                dateTimeTR = dateTimeTRDetail.toString("yyyy-MM-dd HH:mm:ss")
                alarmTitle = self.editDialog.alarmTitleEdit.text()
                alarmDetail = self.editDialog.alarmDetailEdit.toPlainText()
                dataList = [dateTime_, dateTimeTR, alarmTitle, alarmDetail,
                            currentUserID, result[0], result[1], result[2], result[3]]

                # update the AlarmTable and set new values to each column
                # within a chosen row where details are specified
                with self.db:
                    self.c.execute(
                        "UPDATE AlarmTable SET datetime_ = ?, datetimeToRing = ?, title = ?, particular = ? \
                        WHERE userID = ? AND datetime_ = ? AND datetimeToRing = ? AND title = ? AND particular = ?", tuple(dataList))

                self.populateTable()  # populate and update the table

    # remove a row
    def removeRow(self):
        global currentUserID

        row = self.listTable.currentRow()

        # if no row is clicked
        if row == -1:
            QMessageBox.warning(self, "Action Error",
                                "Please SELECT a ROW!", QMessageBox.Ok)
        else:
            choice = QMessageBox.question(self, "Delete Alarm Record",
                                          "Are you sure that you want to delete this record?", QMessageBox.Yes | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:

                # get the dateTime string from the selected row in the table
                dateTime_Item = self.listTable.item(row, 1)
                dateTime_ = dateTime_Item.text()

                # delete the row data in the AlarmTable where userID and
                # dateTime_ meets the binding value
                with self.db:
                    self.c.execute(
                        "DELETE FROM AlarmTable WHERE userID = ? AND dateTime_ = ?", (currentUserID, dateTime_))
                self.populateTable()  # populate and update the table

                # inform user about successfuly deletion of alarm
                QMessageBox.information(self, "Information", f"Your Alarm record for {dateTime_} has been deleted!", QMessageBox.Ok)

# inherit QCalendarWidget to create my custom calendarWidget class


class CalendarWidget(QCalendarWidget):

    # update the paintCell method of QCalendarWidget
    def paintCell(self, painter, rect, date):
        global currentUserID

        # establish database connection
        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        # execure SQL command to find currentUser's dates saved with details
        # from the CalendarTable
        with conn:
            c.execute(
                "SELECT date_ FROM CalendarTable WHERE userID = ? AND detail != ?", (currentUserID, ""))
            result = c.fetchall()
            specialday = []  # create a specialday list to store dates with details

            # user for loop to append the dates (converted into QDate object
            # from string) to sepcialday list
            for i in result:
                for j in i:
                    dateT = QtCore.QDate.fromString(j, "yyyy-MM-dd")
                    specialday.append(dateT)

        # prepare painter of calendarwidget
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        # if the dates in current calendarwidget display are found to be in
        # specialday list..
        if date in specialday:

            # use painter to draw a light blue circle on the date's cell in
            # calendar
            painter.setPen(QtCore.Qt.NoPen)
            # set painter brusher color
            painter.setBrush(QtGui.QColor("#33B5E5"))

            # find radius based on the rectangle size of calendar cells
            r = QtCore.QRect(QtCore.QPoint(), min(
                rect.width(), rect.height()) * QtCore.QSize(1, 1))
            r.moveCenter(rect.center())
            painter.drawEllipse(r)  # draw circle

            # since the default number display of calendarWidget of the cell will be blocked by the new circle
            # use painter to draw text in black color based on the date's day
            painter.setPen(QtGui.QPen(QtGui.QColor("black")))
            painter.drawText(rect, QtCore.Qt.AlignCenter, str(date.day()))
            painter.restore()

        # if dates not in specialday, display default representation of dates
        # in QCalendarWidget using its default paintCell mehotd
        else:
            QCalendarWidget.paintCell(self, painter, rect, date)

# create a main Calendar widget inherited from QWidget class


class Calendar(QWidget):

    # define constructor of the widget
    def __init__(self, parent=None):
        super(Calendar, self).__init__(parent)

        # create an object called calendar from the custom CalendarWidget class
        # created above
        self.calendar = CalendarWidget()
        self.calendar.setStyle(QStyleFactory.create("WindowsVista"))
        self.editor = QTextEdit()
        self.colorButton = QPushButton("Color")

        self.fontButton = QPushButton("Font")
        self.clearButton = QPushButton("Clear Text")
        self.saveButtonCalendar = QPushButton("Save")
        self.counter = 0
        self.calendarUiSetup()  # Calendar widget layout setup

    # Calendar widget layout setup
    def calendarUiSetup(self):
        font = QtGui.QFont()
        font.setPointSize(16)

        self.mainvbox = QVBoxLayout()
        self.miniHlayout1 = QHBoxLayout()
        self.miniHlayout2 = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.calendarGroup = QGroupBox("Calendar")
        self.editorGroup = QGroupBox("Date Particulars")
        self.buttonGroup = QGroupBox("Action Buttons")

        self.calendar.setGridVisible(True)
        self.calendar.setFirstDayOfWeek(1)
        # call showText method when a date on calendar is clicked
        self.calendar.clicked[QtCore.QDate].connect(self.showText)

        self.editor.setFont(font)
        self.editor.setStyleSheet("color: green")

        # assign functions to call for the following buttons when being clicked
        self.colorButton.clicked.connect(
            lambda: self.openDialogFunc(self.colorButton))
        self.fontButton.clicked.connect(
            lambda: self.openDialogFunc(self.fontButton))
        self.clearButton.clicked.connect(lambda: self.editor.setText(""))
        self.saveButtonCalendar.clicked.connect(self.calendarTextSave)

        for item in [self.colorButton, self.fontButton, self.clearButton, self.saveButtonCalendar]:
            self.vbox.addWidget(item)

        self.miniHlayout1.addWidget(self.calendar)
        self.calendarGroup.setLayout(self.miniHlayout1)
        self.miniHlayout2.addWidget(self.editor)
        self.editorGroup.setLayout(self.miniHlayout2)
        self.hbox.addWidget(self.editorGroup)

        self.buttonGroup.setLayout(self.vbox)
        self.hbox.addWidget(self.buttonGroup)
        self.mainvbox.addWidget(self.calendarGroup)
        self.mainvbox.addLayout(self.hbox)
        self.setLayout(self.mainvbox)

    #showText in textEditor
    def showText(self):
        self.counter += 1  # increase counter when a date is clicked
        global currentUserID
        # get current selected date in calendar
        self.date = self.calendar.selectedDate()
        # convert the date into string form to get query result from database
        self.dateTextForRecord = self.date.toString('yyyy-MM-dd')
        # convert date to string to display in editor
        self.dateText = self.date.toString()

        # create connection to data.db and a query object to execute SQL
        # command
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('data.db')
        db.open()
        query = QSqlQuery()
        sql = "SELECT * FROM CalendarTable WHERE userID = '%s' AND date_ = '%s'" % (
            currentUserID, self.dateTextForRecord)
        query.exec_(sql)

        # if no data is found from the current userID and the selected date
        if not query.next():
            # set editor to display the current selected
            self.editor.setText(self.dateText)

        else:
            # if data is found, set the editor text to the query result's text
            # datail data
            self.editor.setText(query.value(2))

        db.close()  # close connection with data.db

    # save the editor's text of selected dates
    def calendarTextSave(self):

        # if user has not clicked on the dates in calendar yet
        if not self.calendar.hasFocus() and self.counter == 0:
            QMessageBox.warning(self, "Calendar selection error!",
                                "Please select a date in the calendar before clicking SAVE button!", QMessageBox.Ok)

        else:
            global currentUserID
            # get current text in the editor
            self.currentEditorText = self.editor.toPlainText()

            # establish connection with data.db and create a query object to
            # execute SQL command
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName('data.db')
            db.open()
            query = QSqlQuery()

            sql = "SELECT * FROM CalendarTable WHERE userID = '%s' AND date_ = '%s'" % (
                currentUserID, self.dateTextForRecord)
            query.exec_(sql)

            # if no previous data of the date and userID, insert new row in the
            # CalendarTable in the database
            if not query.next():
                sql = "INSERT INTO CalendarTable VALUES('%s','%s','%s')" % (
                    currentUserID, self.dateTextForRecord, self.currentEditorText)
                query.exec_(sql)

            # if previous data is found, update the data in databse instead
            else:

                # if the editor text is empty for the selected date (cleared by user)\
                # delete the calendar data in database
                if self.currentEditorText == "":
                    sql = "DELETE FROM CalendarTable WHERE userID = '%s' AND date_ = '%s'" % (
                        currentUserID, self.dateTextForRecord)

                # update if there are contents in editor
                else:
                    sql = "UPDATE CalendarTable SET detail = '%s' WHERE userID = '%s' AND date_ = '%s'" % (
                        self.currentEditorText, currentUserID, self.dateTextForRecord)
                query.exec_(sql)

            db.commit()  # commit to update changes (save) in database
            db.close()  # close database connection with data.db

            # display successful update messageBox to inform user about the
            # process
            QMessageBox.information(self.parent().parent(), "Details Updated",
                                    f"""Your {self.dateTextForRecord} detail has been updated to
{self.currentEditorText}""", QMessageBox.Ok)

    # openDialogFunction, will open colorDialog or fontDialog when colorButton or fontButton
    # update text's font and color in editor based on user's choice in the
    # dialog windwos
    def openDialogFunc(self, button):
        if button == self.colorButton:
            color = QColorDialog.getColor()
            if color.isValid():
                self.editor.setTextColor(color)
        else:
            font, ok = QFontDialog.getFont()
            if ok:
                self.editor.setFont(font)

# create a Memo class inherited from QWidget class


class Memo(QWidget):

    # define constructor of Memo class
    def __init__(self, parent=None):
        # retain default attributes and methods in QWidget's __init__
        # constructor
        super(Memo, self).__init__(parent)

        # create connection class to data.db database file
        # create a c cursor object for the connection to execute SQL commands
        self.db = sqlite3.connect("data.db")
        self.c = self.db.cursor()

        # create a table widget and buttons with specific functions
        self.listTable = QTableWidget()
        self.listTable.setShowGrid(False)
        self.listTable.setEditTriggers(QTableView.NoEditTriggers)
        self.listTable.setAlternatingRowColors(True)
        self.listTable.setSelectionMode(QTableView.SingleSelection)
        self.listTable.setSelectionBehavior(QTableView.SelectRows)
        self.listTable.horizontalHeader().setStretchLastSection(True)
        self.listTable.setRowCount(0)
        self.listTable.setColumnCount(4)
        self.listTable.setHorizontalHeaderLabels(
            ["User", "Date and Time", "Memo Title", "Memo Details"])
        # hide the column 0 which display the userID (user don't have to
        # interact with it)
        self.listTable.hideColumn(0)

        self.loadButton = QPushButton("LOAD MEMO")
        self.loadButton.clicked.connect(self.populateTable)
        self.addButton = QPushButton("ADD")
        self.addButton.clicked.connect(self.addRow)
        self.editButton = QPushButton("EDIT")
        self.editButton.clicked.connect(self.editRow)
        self.removeButton = QPushButton("REMOVE")
        self.removeButton.clicked.connect(self.removeRow)
        self.memoUiSetup()  # setup Memo's layout

    # reset table when a user is logged out by resetting the row and column
    # counts
    def resetTable(self):
        self.listTable.setRowCount(0)
        self.listTable.setColumnCount(4)

    # Memo's layout setup method
    def memoUiSetup(self):
        self.mainHLayout = QHBoxLayout()
        self.group1 = QGroupBox("Memo Section")
        self.smallHLayout = QHBoxLayout()
        self.group2 = QGroupBox("Action Buttons")
        self.verticalLayout = QVBoxLayout()

        for item in [self.loadButton, self.addButton, self.editButton, self.removeButton]:
            font = QtGui.QFont()
            font.setPointSize(12)
            item.setFont(font)
            item.setStyleSheet("color: green")
            self.verticalLayout.addWidget(item)

        self.group2.setLayout(self.verticalLayout)
        self.smallHLayout.addWidget(self.listTable)
        self.group1.setLayout(self.smallHLayout)
        self.mainHLayout.addWidget(self.group1)
        self.mainHLayout.addWidget(self.group2)
        self.setLayout(self.mainHLayout)

    # populateTable method
    def populateTable(self):
        global currentUserID  # get currentUserID
        self.listTable.horizontalHeader().setStretchLastSection(False)

        # using context manager for self.c to execute SQL command under self.db
        # connection
        with self.db:
            self.c.execute("SELECT * FROM MemoTable WHERE userID = ?",
                           (currentUserID,))
            memoData = self.c.fetchall()

            # set new RowCount of the table according to the rows in query
            # result
            self.listTable.setRowCount(len(memoData))

            # using for loop to fill the table by row and column
            for row, row_data in enumerate(memoData):
                for col, data in enumerate(row_data):
                    newData = QTableWidgetItem(data)
                    newData.setToolTip(f"{data}")
                    self.listTable.setItem(row, col, newData)

        # resize the table's row and column size according to contents
        # setStretchLastSection make sure the table to fill the entire widget
        # layout
        self.listTable.resizeColumnsToContents()
        self.listTable.horizontalHeader().setStretchLastSection(True)
        self.listTable.resizeRowsToContents()

    # add new row
    def addRow(self):
        global currentUserID
        # create a custom inputMemoDialog class imported from dialogClass
        # module
        self.inputDialog = inputMemoDialog(self)

        # execute the dialog window, block interaction of user with the Window
        # class if input/action is not done
        self.inputDialog.exec_()

        # if action in dialog is done..
        if self.inputDialog.state:

            # get inputs from the dialog
            dateTimeDetail = self.inputDialog.dateTimeEdit.dateTime()
            dateTime_ = dateTimeDetail.toString("yyyy-MM-dd HH:mm:ss")
            memoTitle = self.inputDialog.memoTitleEdit.text()
            memoDetail = self.inputDialog.memoDetailEdit.toPlainText()
            dataList = [currentUserID, dateTime_, memoTitle, memoDetail]

            # run SQL command to insert new row of data into MemoTable of
            # database file
            with self.db:
                self.c.execute("INSERT INTO MemoTable VALUES (?,?,?,?)",
                               tuple(dataList))

            # call populateTable to fill the table with new data
            self.populateTable()

    # edit certain row on table
    def editRow(self):

        global currentUserID

        # get the current selected row in the table, will return -1 if no row
        # is clicekd
        row = self.listTable.currentRow()

        # if no row is clicked..
        if row == -1:
            QMessageBox.warning(self, "Action Error",
                                "Please SELECT a ROW!", QMessageBox.Ok)
        else:

            # get the datetime string of the selected row to be used in SQL
            # query
            dateTime_Item = self.listTable.item(row, 1)
            dateTime_ = dateTime_Item.text()

            # search for and obtain dateTime, title and detail of a Memo based
            # on current userID and datetime string
            with self.db:
                self.c.execute("SELECT datetime_,title,detail FROM MemoTable WHERE userID = ? AND datetime_ = ?",
                               (currentUserID, dateTime_))
                result = self.c.fetchone()

            # create a custom editMemoDialog imported from dialogClass module
            # pass datetime_ , title and detail of the Memo to the
            # editMemoDialog to be displayed in its widgets
            self.editDialog = editMemoDialog(
                result[0], result[1], result[2], self)
            self.editDialog.exec_()

            # if action in dialog is done..
            if self.editDialog.state:

                # get updated detail from the dialog window
                dateTimeDetail = self.editDialog.dateTimeEdit.dateTime()
                dateTime_ = dateTimeDetail.toString("yyyy-MM-dd HH:mm:ss")
                memoTitle = self.editDialog.memoTitleEdit.text()
                memoDetail = self.editDialog.memoDetailEdit.toPlainText()
                dataList = [dateTime_, memoTitle, memoDetail,
                            currentUserID, result[0], result[1], result[2]]

                # update the selected memo data row in MemoTable based on new
                # details
                with self.db:
                    self.c.execute(
                        "UPDATE MemoTable SET datetime_ = ?, title = ?, detail = ? WHERE userID = ? AND datetime_ = ? AND title = ? AND detail = ?", tuple(dataList))

                self.populateTable()  # fill and update the table

    # remove a row
    def removeRow(self):
        global currentUserID
        row = self.listTable.currentRow()

        # row selection validation
        if row == -1:
            QMessageBox.warning(self, "Action Error",
                                "Please SELECT a ROW!", QMessageBox.Ok)
        else:
            # ask user if he really wants to delete the selected row
            choice = QMessageBox.question(
                self, "Delete Memo Record", "Are you sure that you want to delete this record?", QMessageBox.Yes | QMessageBox.Cancel)
            # if user clicked Yes..
            if choice == QMessageBox.Yes:

                # get dateTime string from the selected row
                dateTime_Item = self.listTable.item(row, 1)
                dateTime_ = dateTime_Item.text()

                # delete the memo data in MemoTable where the userID match
                # currentUserID and the selected datetime string
                with self.db:
                    self.c.execute(
                        "DELETE FROM MemoTable WHERE userID = ? AND dateTime_ = ?", (currentUserID, dateTime_))
                self.populateTable()  # populate table after deletion
                QMessageBox.information(self, "Information", f"Your Memo record for {dateTime_} has been deleted!", QMessageBox.Ok)

# inherit QWidget class for Browser class


class Browser(QWidget):

    # define constructor of Browser class
    def __init__(self, parent=None):
        # retain attributes and methods of QWidget class' __init__ method
        super(Browser, self).__init__(parent)
        # create a QWebEngineView object(PyQt5 browser package) in the name of
        # widget
        self.widget = QWebEngineView()
        self.buttonInit()  # initialize buttons for web browser
        self.browserUiSetup()  # setup Browser layout
        self.browserInit()  # initialize browser's webpage when being opened

    # layout setup method for Browser class
    def browserUiSetup(self):
        self.mainVLayout = QVBoxLayout()
        self.hlayout = QHBoxLayout()
        self.hlayout.setSpacing(0)

        self.lineEditURL = QLineEdit()
        self.lineEditURL.setFixedWidth(600)
        self.label = QLabel("Enter URL: ")
        self.hlayout.addWidget(self.backButton)
        self.hlayout.addWidget(self.forwardButton)
        self.hlayout.addWidget(self.refreshButton)
        self.hlayout.addWidget(self.chromeButton)
        self.hlayout.addStretch(1)
        self.hlayout.addWidget(self.label)
        self.hlayout.addWidget(self.lineEditURL)
        self.hlayout.addWidget(self.push)
        self.hlayout.addStretch(1)
        self.hlayout.addWidget(self.zoomInButton)
        self.hlayout.addWidget(self.zoomOutButton)
        self.mainVLayout.addLayout(self.hlayout)
        self.mainVLayout.addWidget(self.widget)
        self.setLayout(self.mainVLayout)

    # initialize buttons and assign them to call respective methods when being
    # clicked
    def buttonInit(self):
        self.push = QPushButton("GoTo")
        self.backButton = QPushButton()
        self.forwardButton = QPushButton()
        self.refreshButton = QPushButton()
        self.chromeButton = QPushButton()
        self.zoomInButton = QPushButton()
        self.zoomOutButton = QPushButton()
        self.backButton.setIcon(QtGui.QIcon('icons\\back.png'))
        self.forwardButton.setIcon(QtGui.QIcon('icons\\forward.png'))
        self.refreshButton.setIcon(QtGui.QIcon('icons\\refresh.png'))
        self.chromeButton.setIcon(QtGui.QIcon('icons\\search.png'))
        self.zoomInButton.setIcon(QtGui.QIcon('icons\\zoom_in.png'))
        self.zoomOutButton.setIcon(QtGui.QIcon('icons\\zoom_out.png'))
        self.push.clicked.connect(self.displayWebsite)
        self.backButton.clicked.connect(self.widget.back)
        self.forwardButton.clicked.connect(self.widget.forward)
        self.refreshButton.clicked.connect(self.widget.reload)
        self.chromeButton.clicked.connect(self.chromeWebsite)
        self.zoomInButton.clicked.connect(self.zoomInFunc)
        self.zoomOutButton.clicked.connect(self.zoomOutFunc)

    # initialize Browser, show swinburne sarawak website and set URL line edit to current webpage's URL
    # the urlChanged built-in method of QWebEngineView will keep sending
    # signals to enable auto update on the URL display
    def browserInit(self):
        self.widget.load(QtCore.QUrl('https://swinburne.edu.my'))
        self.widget.urlChanged.connect(
            lambda: self.lineEditURL.setText(self.widget.url().toDisplayString()))

    # goTo google website when chromeButton is clicked
    def chromeWebsite(self):
        self.widget.load(QtCore.QUrl("https://google.com"))

    # load the typed URL in lineEdit, include URL validation for https:// and http://
    # auto add https:// in the string if it is not found in user's typed URL
    def displayWebsite(self):
        if self.lineEditURL.text().startswith('https://') or self.lineEditURL.text().startswith('http://'):
            self.widget.load(QtCore.QUrl(self.lineEditURL.text()))
        else:
            self.widget.load(QtCore.QUrl('https://' + self.lineEditURL.text()))

    # zoom in the browser with 0.1 factor
    def zoomInFunc(self):
        self.widget.setZoomFactor(self.widget.zoomFactor() + 0.1)

    # zoom out the browser with - 0.1 factor
    def zoomOutFunc(self):
        self.widget.setZoomFactor(self.widget.zoomFactor() - 0.1)

    # update keyPressEvent of QWidget class, accept QKeyEvent signals
    # include URL validation same  as displayWebsite()
    # will run and load the URL if the key pressed is return key or enter key
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Return or QKeyEvent.key() == QtCore.Qt.Key_Enter:
            if self.lineEditURL.hasFocus():
                if self.lineEditURL.text().startswith('https://') or self.lineEditURL.text().startswith('http://'):
                    self.widget.load(QtCore.QUrl(self.lineEditURL.text()))
                else:
                    self.widget.load(QtCore.QUrl(
                        'https://' + self.lineEditURL.text()))

# inherit QLCDNumber to create a custom DigitalClock class


class DigitalClock(QLCDNumber):

    def __init__(self, parent=None):
        # inherit default attributes and methods in __init__ method of
        # QLCDNumber
        super(DigitalClock, self).__init__(parent)
        self.digitalClockUiSetup()  # call the UI setup for the DigitalClock

    # define digitalClock's UI setup method
    def digitalClockUiSetup(self):
        self.setSegmentStyle(QLCDNumber.Flat)
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet("color: white")
        self.setFixedSize(400, 150)
        timer = QtCore.QTimer(self)  # create timer object
        # timer will trigger showTime() when timeout
        timer.timeout.connect(self.showTime)
        timer.start(1000)  # timer timeout in every seconds, 1000 mS
        self.showTime()  # call showTime() right after timer start to work

    # show current time in the DigitalClock's digit display
    def showTime(self):
        time_ = QtCore.QTime.currentTime()
        text = time_.toString('HH:mm')
        if (time_.second() % 2) == 0:
            # take out colon : whenever second is evenNum, appearing to flicker
            text = text[:2] + ' ' + text[3:]

        # .display is the default method for QLCDNumber to display items (strings/numbers)
        self.display(text)
