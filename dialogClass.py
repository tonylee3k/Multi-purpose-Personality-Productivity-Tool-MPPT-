# import necessary widget classes from PyQt5
from PyQt5.QtWidgets import (
    QDialog,
    QMessageBox,
    QPushButton,
    QLabel,
    QLineEdit,
    QGridLayout,
    QDateTimeEdit,
    QTextEdit,
    QComboBox,
    QDoubleSpinBox)

# import QtCore and QDateTime modules to pull out qt functions and deal
# with time respectively
from PyQt5 import QtCore
from PyQt5.Qt import QDateTime

# alarmRingDialog inherited from QDialog class, shows up when an alarm's
# date&time met curret date&time


class alarmRingDialog(QDialog):

    # define alarmRingDialog's constructor
    # will receive query result from database's AlarmTable
    # args (will be accepting a list, so no need use *args to unpack query
    # results)
    def __init__(self, args, parent=None):
        # retain the default attributes and methods of QDialog constructor
        super(alarmRingDialog, self).__init__(parent)

        self.closedState = False  # indicate dialog window is NOT closed

        # create necessary widgets for this dialog and set its window modality
        self.setWindowTitle("Alarm")
        self.setWindowModality(QtCore.Qt.NonModal)
        self.dateTimeEditLabel = QLabel("Date and Time: ")
        self.dateTimeEdit = QLineEdit()
        self.dateTimeTREditLabel = QLabel("Date and Time Ringed: ")
        self.dateTimeTREdit = QLineEdit()
        self.alarmTitleEditLabel = QLabel("Alarm Title: ")
        self.alarmTitleEdit = QLineEdit()
        self.alarmDetailEditLabel = QLabel("Alarm Details: ")
        self.alarmDetailEdit = QTextEdit()
        self.inputButton = QPushButton("Okay")
        # call ok function when Okay button is clicked
        self.inputButton.clicked.connect(self.ok)

        for edit in [self.dateTimeEdit, self.dateTimeTREdit, self.alarmTitleEdit, self.alarmDetailEdit]:
            edit.setReadOnly(True)

        # set following widgets' display value according to query result
        self.dateTimeEdit.setText(args[0])
        self.dateTimeTREdit.setText(args[1])
        self.alarmTitleEdit.setText(args[2])
        self.alarmDetailEdit.setText(args[3])
        self.alarmRingSetup()  # call its own layout setup method

    # alarmRingDialog layout setup
    def alarmRingSetup(self):
        self.formLayout = QGridLayout()
        self.formLayout.setSpacing(10)
        self.formLayout.addWidget(self.dateTimeEditLabel, 0, 0)
        self.formLayout.addWidget(self.dateTimeEdit, 0, 1)
        self.formLayout.addWidget(self.dateTimeTREditLabel, 1, 0)
        self.formLayout.addWidget(self.dateTimeTREdit, 1, 1)
        self.formLayout.addWidget(self.alarmTitleEditLabel, 2, 0)
        self.formLayout.addWidget(self.alarmTitleEdit, 2, 1)
        self.formLayout.addWidget(self.alarmDetailEditLabel, 3, 0)
        self.formLayout.addWidget(self.alarmDetailEdit, 3, 1, 6, 2)
        self.formLayout.addWidget(self.inputButton, 7, 0)
        self.setLayout(self.formLayout)

    # close the dialog when Ok button is clicked, update closedState
    def ok(self):
        self.close()
        self.closedState = True

    # update closedState too in case user clicked "X" to close dialog window
    def closeEvent(self, QCloseEvent):
        self.closedState = True

# inherit QDialog class for inputMemoDialog


class inputMemoDialog(QDialog):

    # define class constructor
    def __init__(self, parent=None):
        super(inputMemoDialog, self).__init__(parent)
        # self.state indicate actions in this QDialog is not done yet (User
        # didn't click Okay button)
        self.state = False

        # create necessary widgets for inputMemoDialog and set its window
        # modality
        self.setWindowTitle("Memo Details Input")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.dateTimeEditLabel = QLabel("Select Date and Time: ")
        self.dateTimeEdit = QDateTimeEdit(QDateTime.currentDateTime())
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit.setCalendarPopup(True)
        self.memoTitleEditLabel = QLabel("Input Memo Title: ")
        self.memoTitleEdit = QLineEdit()
        self.memoDetailEditLabel = QLabel("Input Memo Details: ")
        self.memoDetailEdit = QTextEdit()
        self.inputButton = QPushButton("Okay")
        # call addInput function when Okay button is clicked
        self.inputButton.clicked.connect(self.addInput)
        self.inputMemoDialogSetup()  # call its own layout setup method

    # inputMemoDialog layout setup
    def inputMemoDialogSetup(self):
        self.formLayout = QGridLayout()
        self.formLayout.setSpacing(10)
        self.formLayout.addWidget(self.dateTimeEditLabel, 0, 0)
        self.formLayout.addWidget(self.dateTimeEdit, 0, 1)
        self.formLayout.addWidget(self.memoTitleEditLabel, 1, 0)
        self.formLayout.addWidget(self.memoTitleEdit, 1, 1)
        self.formLayout.addWidget(self.memoDetailEditLabel, 2, 0)
        self.formLayout.addWidget(self.memoDetailEdit, 2, 1, 5, 2)
        self.formLayout.addWidget(self.inputButton, 6, 0)
        self.setLayout(self.formLayout)

    # check if user fulfil input validation and close window if requirement is met
    # also update state to True indicate action is done in this dialog window
    # when user clicked okay button
    def addInput(self):
        memoTitle = self.memoTitleEdit.text()
        memoDetail = self.memoDetailEdit.toPlainText()
        if memoTitle == "" or memoDetail == "":
            QMessageBox.warning(self, "Input Error",
                                "Please don't leave BLANK!", QMessageBox.Ok)
        else:
            self.close()
            self.state = True

    # SET state to False, indicating action is not done as
    # user clicked "X" to close the dialog
    def closeEvent(self, QCloseEvent):
        self.state = False

# Inherit QDialog class for inputAlarmDialog


class inputAlarmDialog(QDialog):

    # define constructor for inputAlarmDialog
    def __init__(self, parent=None):
        super(inputAlarmDialog, self).__init__(parent)
        self.state = False  # indicate action is not done

        # create necessary widgets and set dialog windows' modality
        self.setWindowTitle("Alarm Details Input")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.dateTimeEdit = QDateTimeEdit(QDateTime.currentDateTime())
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit.setCalendarPopup(True)
        self.dateTimeEdit.setReadOnly(True)
        self.dateTimeTREditLabel = QLabel("Select Date and Time to Ring: ")
        self.dateTimeTREdit = QDateTimeEdit(QDateTime.currentDateTime())
        self.dateTimeTREdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeTREdit.setCalendarPopup(True)
        self.alarmTitleEditLabel = QLabel("Input Memo Title: ")
        self.alarmTitleEdit = QLineEdit()
        self.alarmDetailEditLabel = QLabel("Input Memo Details: ")
        self.alarmDetailEdit = QTextEdit()
        self.inputButton = QPushButton("Okay")
        self.inputButton.clicked.connect(self.addInput)
        self.inputAlarmDialogSetup()  # call its own layout setup method

    # inputAlarmDialog layout setup
    def inputAlarmDialogSetup(self):
        self.formLayout = QGridLayout()
        self.formLayout.setSpacing(10)
        self.formLayout.addWidget(self.dateTimeTREditLabel, 0, 0)
        self.formLayout.addWidget(self.dateTimeTREdit, 0, 1)
        self.formLayout.addWidget(self.alarmTitleEditLabel, 1, 0)
        self.formLayout.addWidget(self.alarmTitleEdit, 1, 1)
        self.formLayout.addWidget(self.alarmDetailEditLabel, 2, 0)
        self.formLayout.addWidget(self.alarmDetailEdit, 2, 1, 5, 2)
        self.formLayout.addWidget(self.inputButton, 6, 0)
        self.setLayout(self.formLayout)

    # check input validity and close dialog window + set state to True, indicate action is done
    # when user clicked okay button
    def addInput(self):
        alarmTitle = self.alarmTitleEdit.text()
        alarmDetail = self.alarmDetailEdit.toPlainText()
        if alarmTitle == "" or alarmDetail == "":
            QMessageBox.warning(self, "Input Error",
                                "Please don't leave BLANK!", QMessageBox.Ok)
        else:
            self.close()
            self.state = True

    # set state to False when 'X' is clicked, indicate action is not done
    def closeEvent(self, QCloseEvent):
        self.state = False

# inherit QDialog class for editMemoDialog


class editMemoDialog(QDialog):

    # define constructor for editMemoDialog
    # pass query result from MemoTable in database to the dialog, *args will
    # unpack the three query results
    def __init__(self, *args, parent=None):
        super(editMemoDialog, self).__init__(parent)
        self.state = False  # indicate action is not done

        # create necessary widgets for editMemoDialog
        self.setWindowTitle("Memo Details Edit")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.dateTimeEditLabel = QLabel("Select Date and Time: ")
        self.dateTimeEdit = QDateTimeEdit(QDateTime.currentDateTime())
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit.setCalendarPopup(True)
        self.memoTitleEditLabel = QLabel("Input Memo Title: ")
        self.memoTitleEdit = QLineEdit()
        self.memoDetailEditLabel = QLabel("Input Memo Details: ")
        self.memoDetailEdit = QTextEdit()
        self.inputButton = QPushButton("Okay")
        self.inputButton.clicked.connect(self.addInput)

        # set the following 3 widgets' values according to query result
        self.dateTimeEdit.setDateTime(
            QtCore.QDateTime.fromString(args[0], 'yyyy-MM-dd HH:mm:ss'))
        self.memoTitleEdit.setText(args[1])
        self.memoDetailEdit.setText(args[2])
        self.editMemoDialogSetup()  # call its own layout setup method

    # editMemoDialog layout setup method
    def editMemoDialogSetup(self):
        self.formLayout = QGridLayout()
        self.formLayout.setSpacing(10)
        self.formLayout.addWidget(self.dateTimeEditLabel, 0, 0)
        self.formLayout.addWidget(self.dateTimeEdit, 0, 1)
        self.formLayout.addWidget(self.memoTitleEditLabel, 1, 0)
        self.formLayout.addWidget(self.memoTitleEdit, 1, 1)
        self.formLayout.addWidget(self.memoDetailEditLabel, 2, 0)
        self.formLayout.addWidget(self.memoDetailEdit, 2, 1, 5, 2)
        self.formLayout.addWidget(self.inputButton, 6, 0)
        self.setLayout(self.formLayout)

    # input validation for title and details of a selected memo in edit dialog
    # close the dialog and update the sate to True, indicate action is done
    # when user clicked Okay button
    def addInput(self):
        memoTitle = self.memoTitleEdit.text()
        memoDetail = self.memoDetailEdit.toPlainText()
        if memoTitle == "" or memoDetail == "":
            QMessageBox.warning(self, "Input Error",
                                "Please don't leave BLANK!", QMessageBox.Ok)
        else:
            self.close()
            self.state = True

    # set state to False, indicate action is not done if user clicked "x" to
    # quit the dialog
    def closeEvent(self, QCloseEvent):
        self.state = False

# inherit QDialog class for editAlarmDialog


class editAlarmDialog(QDialog):

    # define constructor for editAlarmDialog, pass query result from AlarmTable to the dialog
    #*args will unpack the query result
    def __init__(self, *args, parent=None):
        super(editAlarmDialog, self).__init__(parent)
        self.state = False  # indicate action is not done

        # create necessary widgets for editAlarmDialog
        self.setWindowTitle("Alarm Details Edit")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.dateTimeEditLabel = QLabel("Date and Time: ")
        self.dateTimeEdit = QDateTimeEdit(QDateTime.currentDateTime())
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit.setCalendarPopup(True)
        self.dateTimeTREditLabel = QLabel("Select Date and Time to Ring: ")
        self.dateTimeTREdit = QDateTimeEdit(QDateTime.currentDateTime())
        self.dateTimeTREdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeTREdit.setCalendarPopup(True)
        self.alarmTitleEditLabel = QLabel("Input Alarm Title: ")
        self.alarmTitleEdit = QLineEdit()
        self.alarmDetailEditLabel = QLabel("Input Alarm Details: ")
        self.alarmDetailEdit = QTextEdit()
        self.inputButton = QPushButton("Okay")
        self.inputButton.clicked.connect(self.addInput)

        # set the following widgets' values according to the query results
        self.dateTimeEdit.setDateTime(
            QtCore.QDateTime.fromString(args[0], 'yyyy-MM-dd HH:mm:ss'))
        self.dateTimeTREdit.setDateTime(
            QtCore.QDateTime.fromString(args[1], 'yyyy-MM-dd HH:mm:ss'))
        self.alarmTitleEdit.setText(args[2])
        self.alarmDetailEdit.setText(args[3])
        self.editAlarmDialogSetup()  # call its own layout setup method

    # define layout setup method for editAlarmDialog
    def editAlarmDialogSetup(self):
        self.formLayout = QGridLayout()
        self.formLayout.setSpacing(10)
        self.formLayout.addWidget(self.dateTimeEditLabel, 0, 0)
        self.formLayout.addWidget(self.dateTimeEdit, 0, 1)
        self.formLayout.addWidget(self.dateTimeTREditLabel, 1, 0)
        self.formLayout.addWidget(self.dateTimeTREdit, 1, 1)
        self.formLayout.addWidget(self.alarmTitleEditLabel, 2, 0)
        self.formLayout.addWidget(self.alarmTitleEdit, 2, 1)
        self.formLayout.addWidget(self.alarmDetailEditLabel, 3, 0)
        self.formLayout.addWidget(self.alarmDetailEdit, 3, 1, 6, 2)
        self.formLayout.addWidget(self.inputButton, 7, 0)
        self.setLayout(self.formLayout)

    # user input validation for selected alarm's titel and detail
    # close the dialog and set state to True, indicate action is done when
    # user clicked Okay button
    def addInput(self):
        alarmTitle = self.alarmTitleEdit.text()
        alarmDetail = self.alarmDetailEdit.toPlainText()
        if alarmTitle == "" or alarmDetail == "":
            QMessageBox.warning(self, "Input Error",
                                "Please don't leave BLANK!", QMessageBox.Ok)
        else:
            self.close()
            self.state = True

    # set the state to False when user clicked 'x' to close the dialog window,
    # indicate action is not done
    def closeEvent(self, QCloseEvent):
        self.state = False

# inherit QDialog class for inputBudgetDialog


class inputBudgetDialog(QDialog):

    # define class constructor for inputBudgetDialog, selected table will be passed into table parameters,
    # yM will receive yearMonth in string to set dateEdit's value via
    # .fromString() method
    def __init__(self, table, yM, parent=None):
        super(inputBudgetDialog, self).__init__(parent)
        self.state = False  # indicate action is not done

        # create necessary widgets for inputBudgetDialog
        self.setWindowTitle("Budget details input")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.yearMonth = yM
        self.dataTypeLabel = QLabel("Select accounting entry: ")
        self.dataType = QLineEdit()

        # table checks
        self.dataType.setText("debit") if table == self.parent(
        ).debitTable else self.dataType.setText("credit")

        self.dataType.setReadOnly(True)
        self.dateEditLabel = QLabel("Select a date: ")
        self.dateEdit = QDateTimeEdit(QDateTime.currentDateTime())
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.particularLabel = QLabel("Input particular: ")
        self.particularEdit = QLineEdit()
        self.referenceLabel = QLabel("Input reference: ")
        self.referenceEdit = QLineEdit()
        self.amountLabel = QLabel("Enter Amount(RM): ")
        self.amountEdit = QDoubleSpinBox()
        self.amountEdit.setRange(0, 1000000)
        self.amountEdit.setDecimals(2)
        self.amountEdit.setPrefix("RM")
        self.amountEdit.setValue(0)

        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clearText)
        self.okButton = QPushButton("Ok")
        self.okButton.clicked.connect(self.addInput)

        self.inputBudgetSetup()  # call its layout setup method

    # inputBudgetDialog's layout setup method
    def inputBudgetSetup(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.dataTypeLabel, 0, 0)
        self.grid.addWidget(self.dataType, 0, 1)
        self.grid.addWidget(self.dateEditLabel, 1, 0)
        self.grid.addWidget(self.dateEdit, 1, 1)
        self.grid.addWidget(self.particularLabel, 2, 0)
        self.grid.addWidget(self.particularEdit, 2, 1)
        self.grid.addWidget(self.referenceLabel, 3, 0)
        self.grid.addWidget(self.referenceEdit, 3, 1)
        self.grid.addWidget(self.amountLabel, 4, 0)
        self.grid.addWidget(self.amountEdit, 4, 1)
        self.grid.addWidget(self.clearButton, 5, 0)
        self.grid.addWidget(self.okButton, 5, 1)
        self.setLayout(self.grid)

    # reset input details to default when clear button is clicked
    def clearText(self):
        self.particularEdit.setText("")
        self.referenceEdit.setText("")
        self.amountEdit.setValue(0)

    # user input validation for yearMonth, budget particular and budget amount, only reference can be leave as blank
    # close the dialog and set state to True, indicate action is done
    def addInput(self):
        yearMonth = self.dateEdit.dateTime().toString("yyyy-MM")
        particular = self.particularEdit.text()
        amount = self.amountEdit.value()

        if yearMonth != self.yearMonth:
            QMessageBox.warning(self, "Year Month Error!", f"Please only add new budget record for {self.yearMonth}!", QMessageBox.Ok)

        elif particular == "":
            QMessageBox.warning(
                self, "Input Error!", "Please don't leave PARTICULAR as BLANK!", QMessageBox.Ok)
        elif amount == 0:
            button = QMessageBox.question(
                self, "Input Value", "Are you sure you want to set amount to RM0 ?", QMessageBox.Yes | QMessageBox.No)
            if button == QMessageBox.Yes:
                self.close()
                self.state = True
            else:
                pass
        else:
            self.close()
            self.state = True

    # set the state to False, indicate action is not done if user clicked "x"
    # to close the dialog window
    def closeEvent(self, QCloseEvent):
        self.state = False

# inherit QDialog class for editBudgetDialog


class editBudgetDialog(QDialog):

    # define constructor for editBudgetDialog, args will receive a list of
    # items from query result
    def __init__(self, args, parent=None):
        super(editBudgetDialog, self).__init__(parent)

        # set the dialog state to False, indicate action is not done
        self.state = False

        # create necessary widgets for editBudgetDialog
        self.setWindowTitle("Budget Details Edit")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.yearMonthLabel = QLabel("Select Year and Month: ")
        self.yearMonthEdit = QDateTimeEdit()
        self.yearMonthEdit.setDisplayFormat("yyyy-MM")
        self.dataTypeLabel = QLabel("Select accounting entry: ")
        self.dataType = QComboBox()
        self.dataType.addItems(["debit", "credit"])
        self.dateEditLabel = QLabel("Select a date: ")
        self.dateEdit = QDateTimeEdit(QDateTime.currentDateTime())
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.particularLabel = QLabel("Input particular: ")
        self.particularEdit = QLineEdit()
        self.referenceLabel = QLabel("Input reference: ")
        self.referenceEdit = QLineEdit()
        self.amountLabel = QLabel("Enter Amount(RM): ")
        self.amountEdit = QDoubleSpinBox()
        self.amountEdit.setRange(0, 1000000)
        self.amountEdit.setDecimals(2)
        self.amountEdit.setPrefix("RM")
        self.amountEdit.setValue(0)

        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clearText)
        self.okButton = QPushButton("Ok")
        self.okButton.clicked.connect(self.addInput)

        # set the values of following widgets according to query result
        self.yearMonthEdit.setDateTime(
            QDateTime.fromString(args[1], 'yyyy-MM'))
        self.dataType.setCurrentIndex(
            0) if args[2] == "debit" else self.dataType.setCurrentIndex(1)
        self.dateEdit.setDateTime(QDateTime.fromString(args[3], 'yyyy-MM-dd'))
        self.particularEdit.setText(args[4])
        self.referenceEdit.setText(args[5])
        self.amountEdit.setValue(float(args[6]))

        self.editBudgetSetup()  # call its own method for layout setup

    # define layout setup method for editBudgetDialog
    def editBudgetSetup(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.yearMonthLabel, 0, 0)
        self.grid.addWidget(self.yearMonthEdit, 0, 1)
        self.grid.addWidget(self.dataTypeLabel, 1, 0)
        self.grid.addWidget(self.dataType, 1, 1)
        self.grid.addWidget(self.dateEditLabel, 2, 0)
        self.grid.addWidget(self.dateEdit, 2, 1)
        self.grid.addWidget(self.particularLabel, 3, 0)
        self.grid.addWidget(self.particularEdit, 3, 1)
        self.grid.addWidget(self.referenceLabel, 4, 0)
        self.grid.addWidget(self.referenceEdit, 4, 1)
        self.grid.addWidget(self.amountLabel, 5, 0)
        self.grid.addWidget(self.amountEdit, 5, 1)
        self.grid.addWidget(self.clearButton, 6, 0)
        self.grid.addWidget(self.okButton, 6, 1)
        self.setLayout(self.grid)

    # set selected budget's particular, reference and amount to default value
    def clearText(self):
        self.particularEdit.setText("")
        self.referenceEdit.setText("")
        self.amountEdit.setValue(0)

    # user input validation
    # close the dialog when user clicked Okay button
    # editBudgetDialog will prompt user for RM0 input for double confirmation
    # set state to True, indicate action is done
    def addInput(self):
        particular = self.particularEdit.text()
        amount = self.amountEdit.value()

        if particular == "":
            QMessageBox.warning(
                self, "Input Error!", "Please don't leave PARTICULAR as BLANK!", QMessageBox.Ok)
        elif amount == 0.00:
            button = QMessageBox.question(
                self, "Input Value", "Are you sure you want to set amount to RM0 ?", QMessageBox.Yes | QMessageBox.No)
            if button == QMessageBox.Yes:
                self.close()
                self.state = True
        else:
            self.close()
            self.state = True

    # set state to False, indicate action is not done if user clicked 'x' to
    # close the dialog window
    def closeEvent(self, QCloseEvent):
        self.state = False
