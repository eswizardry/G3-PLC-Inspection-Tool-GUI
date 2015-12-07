#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: eswizardry
# @Date:   2015-12-02 22:15:29
# @Last Modified by:   eswizardry
# @Last Modified time: 2015-12-07 16:38:08
"""
G3-PLC Module Inspection Tool v0.1
"""
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

#List of test rack & test rack name
testRack          = ['No.1', 'No.2', 'No.3', 'No.4', 'No.5', 'No.6', 'No.7', 'No.8', 'No.9']

#============================== CONST DEFINE ==================================
APP_NAME          = 'G3-PLC Module Inspection Tool '
APP_VERSION       = 'v0.1'
TICK_PERIOD       = 1000
BUTTON_WIDTH      = 300
BUTTON_HEIGHT     = 50
PBAR_HEIGHT       = 20
TIME_FRAME_WIDTH  = 395
RACK_FRAME_WIDTH  = 50
RACK_FRAME_HEIGHT = 100
MAINWINDOW_WIDTH  = 1200
MAINWINDOW_HEIGHT = 400
PBAR_VAL_100      = 100
PBAR_VAL_0        = 0

class RackPos:
    """docstring for ClassName"""
    FIRST   = 0
    SECOND  = 1
    THIRD   = 2
    FOURTH  = 3
    FIFTH   = 5
    SIXTH   = 6
    SEVENTH = 7
    EIGHTH  = 8
    NINTH   = 9

class RackStatus:
    """docstring for ClassName"""
    DEFAULT = 0
    JOINED  = 1
    PASSED  = 2
    FAILED  = 3

class PBarStatus:
    """docstring for ClassName"""
    DEAFULT = 0
    BUSY    = 1
    DONE    = 2

#========================= MAIN WINDOW CLASS ==================================
class PLCGui(QMainWindow):
    elapsedTimerStatus = False

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.addGadgetToMainWindow()
        #create central widget for main window
        window = QWidget()
        mainHbox = QHBoxLayout()
        mainHbox.addWidget(self.drawMainLayout())
        window.setLayout(mainHbox)
        # Set QWidget as the central layout of the main window
        self.setCentralWidget(window)

        # Main window
        self.resize(MAINWINDOW_WIDTH, MAINWINDOW_HEIGHT)
        self.centeringWindow()
        self.setWindowTitle(APP_NAME+APP_VERSION)
        self.setWindowIcon(QIcon('rsc\\powericon.png'))

        self.show()

    def drawMainLayout(self):
        #_____________________________________________
        #                                             |
        #                                             |
        #                    MAIN                     |
        #                                             |
        #_____________________________________________|
        #                     |                       |
        #    Bottom Left      |       Bottom Right    |
        #_____________________|_______________________|
        #Main Splitter
        self.mainSplitter = QSplitter(Qt.Vertical)
        self.mainSplitter.addWidget(self.mainFrameLayout())
        self.mainSplitter.addWidget(self.bottomFrameLayout())
        return self.mainSplitter

    def mainFrameLayout(self):
        length = len(testRack)
        self.lbl_testRackNumber = []
        self.lbl_macAddressText = []
        self.lbl_macAddressValue = []
        self.square = []
        self.number_hbox = []
        self.mainframe_vbox = []
        self.progressBar = []
        self.frame = []

        for i in range(0, length):
            #Rack number label
            self.lbl_testRackNumber.append(QLabel(self))
            self.lbl_testRackNumber[i].setText(testRack[i])
            self.lbl_testRackNumber[i].setStyleSheet('''
                QWidget
                {
                    font-family: "Times New Roman", Georgia, Serif;
                    font-weight: bold;
                    font-size: 28px;
                    color: #000000;
                }
                ''')
            #Frame
            self.frame.append(QFrame(self))
            self.frame[i].setFrameStyle(QFrame.WinPanel | QFrame.Sunken)
            #MAC Address text
            self.lbl_macAddressText.append(QLabel(self))
            self.lbl_macAddressText[i].setText('MAC Address:')
            #MAC Address value
            self.lbl_macAddressValue.append(QLabel(self))
            self.lbl_macAddressValue[i].setText('123456789ABCD')
            self.lbl_macAddressValue[i].setStyleSheet('''
                QWidget
                {
                    font-family: "Times New Roman", Georgia, Serif;
                    font-weight: bold;
                    font-size: 14px;
                    color: #000000;
                }
                ''')
            #Progress Bar
            self.progressBar.append(QProgressBar(self))
            self.progressBar[i].setMaximumHeight(PBAR_HEIGHT)
            self.setProgressBarDefault(i)
            #create square for
            self.square.append(QFrame(self))
            self.square[i].setMinimumHeight(RACK_FRAME_HEIGHT)
            self.square[i].setMinimumWidth(RACK_FRAME_WIDTH)
            self.number_hbox.append(QHBoxLayout())
            self.number_hbox[i].addStretch(1)
            self.number_hbox[i].addWidget(self.lbl_testRackNumber[i])
            self.number_hbox[i].addStretch(1)
            self.square[i].setLayout(self.number_hbox[i])
            self.square[i].setStyleSheet("""
                QWidget
                {
                    border-radius: 10px;
                    background-color:#C9CAC9;
                }
                """)

            self.mainframe_vbox.append(QVBoxLayout())
            self.mainframe_vbox[i].addWidget(self.square[i])
            self.mainframe_vbox[i].addWidget(self.progressBar[i])
            self.mainframe_vbox[i].addStretch(1)
            self.mainframe_vbox[i].addWidget(self.lbl_macAddressText[i])
            self.mainframe_vbox[i].addWidget(self.lbl_macAddressValue[i])
            # self.mainframe_vbox[i].addStretch(1)
            self.frame[i].setLayout(self.mainframe_vbox[i])

        self.mainframe_hbox = QHBoxLayout()
        for i in range(0, length):
            self.mainframe_hbox.addWidget(self.frame[i])

        self.mainframe = QFrame(self)
        self.mainframe.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.mainframe.setLayout(self.mainframe_hbox)
        return self.mainframe

    def bottomFrameLayout(self):
        self.bottomSplitter = QSplitter(Qt.Horizontal)
        self.bottomSplitter.addWidget(self.bottomLeftLayout())
        self.bottomSplitter.addWidget(self.bottomRightLayout())
        return self.bottomSplitter

    def bottomLeftLayout(self):
        self.bottomright = QFrame(self)
        self.bottomright.setMaximumWidth(TIME_FRAME_WIDTH)
        self.bottomright.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.lbl_testResult = QLabel(self)
        self.lbl_testResult.setText('Test Time: ')
        self.lbl_testResult.setStyleSheet('''
            QWidget
            {
                font-family: "Times New Roman", Georgia, Serif;
                font-weight: bold;
                font-size: 38px;
                color: #000000;
            }
            ''')

        self.lbl_time = QLabel(self)
        self.lbl_time.setText('00:00:00')
        self.lbl_time.setStyleSheet('''
            QWidget
            {
                font-family: "Times New Roman", Georgia, Serif;
                font-weight: bold;
                font-size: 48px;
                color: #000000;
            }
            ''')

        self.bottomright_hbox = QHBoxLayout()
        self.bottomright_hbox.addWidget(self.lbl_testResult)
        self.bottomright_hbox.addWidget(self.lbl_time)
        self.bottomright_hbox.addStretch(1)
        self.bottomright.setLayout(self.bottomright_hbox)
        return self.bottomright

    def bottomRightLayout(self):
        self.bottomleft = QFrame(self)
        self.bottomleft.setFrameStyle(QFrame.Box | QFrame.Raised)

        self.qbtnJoinDCU = QPushButton('Join DCU (F1)', self)
        self.qbtnJoinDCU.setStyleSheet('''
            QWidget
            {
                font-family: "Times New Roman", Georgia, Serif;
                font-weight: bold;
                font-size: 28px;
                background-color: #FAF105;
                color: #000000;
            }
            ''')
        self.qbtnJoinDCU.setMinimumHeight(BUTTON_HEIGHT)
        self.qbtnJoinDCU.setMaximumWidth(BUTTON_WIDTH)
        self.qbtnJoinDCU.clicked.connect(self.joinNetwork)
        # self.qbtnJoinDCU.resize(self.qbtnJoinDCU.sizeHint())

        self.qbtnCheck = QPushButton('Start Check (F2)', self)
        self.qbtnCheck.setStyleSheet('''
            QWidget
            {
                font-family: "Times New Roman", Georgia, Serif;
                font-weight: bold;
                font-size: 28px;
                background-color: #05D51D;
                color: #000000;
            }
            ''')
        self.qbtnCheck.setMinimumHeight(BUTTON_HEIGHT)
        self.qbtnCheck.setMaximumWidth(BUTTON_WIDTH)
        self.qbtnCheck.clicked.connect(self.checkCommunication)
        # self.qbtnCheck.resize(self.qbtnCheck.sizeHint())

        self.bottomleft_hbox1 = QHBoxLayout()
        self.bottomleft_hbox1.addWidget(self.qbtnJoinDCU)
        self.bottomleft_hbox1.addWidget(self.qbtnCheck)
        # self.bottomleft_hbox1.addStretch(1)
        self.bottomleft_vbox = QVBoxLayout()
        self.bottomleft_vbox.addLayout(self.bottomleft_hbox1)
        # self.bottomleft_vbox.addStretch(1)
        self.bottomleft.setLayout(self.bottomleft_vbox)
        return self.bottomleft

    def centeringWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def addGadgetToMainWindow(self):
        actionExit = self.exitAction()
        actionAbout = self.aboutAction()
        actionJoin = self.joinAction()
        actionCheck = self.checkAction()
        #Add status bar to widget
        self.statusBar()
        #Add menubar to widget
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(actionJoin)
        fileMenu.addAction(actionCheck)
        fileMenu.addAction(actionAbout)
        fileMenu.addAction(actionExit)
        #Add action to toolbar
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(actionJoin)
        toolbar.addAction(actionCheck)
        toolbar.addAction(actionAbout)
        toolbar.addAction(actionExit)

    def exitAction(self):
        exitAction = QAction(QIcon('rsc\\exit-icon.png'), 'Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Quit')
        exitAction.triggered.connect(self.close)
        return exitAction

    def aboutAction(self):
        aboutAction = QAction(QIcon('rsc\\info-icon.png'), 'About', self)
        aboutAction.setShortcut('Ctrl+I')
        aboutAction.setStatusTip('About')
        aboutAction.triggered.connect(self.aboutEvent)
        return aboutAction

    def joinAction(self):
        joinAction = QAction(QIcon('rsc\\join-icon.png'), 'Join Network', self)
        joinAction.setShortcut('F1')
        joinAction.setStatusTip('Join Network')
        joinAction.triggered.connect(self.joinNetwork)
        return joinAction

    def checkAction(self):
        checkAction = QAction(QIcon('rsc\\check-icon.png'), 'Check communication', self)
        checkAction.setShortcut('F2')
        checkAction.setStatusTip('Check communication')
        checkAction.triggered.connect(self.checkCommunication)
        return checkAction

    def aboutEvent(self, event):
        reply = QMessageBox.about(self, 'About',
            '\nG3-PLC Inspection Tool V 0.1\nPowered by Python3 + PyQt5')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def setColorDefault(self, rackPos):
        self.square[rackPos].setStyleSheet("""
            QWidget
            {
                border-radius: 10px;
                background-color:#C9CAC9;
            }
            """)

    def setColorJoined(self, rackPos):
        self.square[rackPos].setStyleSheet("""
            QWidget
            {
                border-radius: 10px;
                background-color:#EEFD04;
            }
            """)

    def setColorPassed(self, rackPos):
        self.square[rackPos].setStyleSheet("""
            QWidget
            {
                border-radius: 10px;
                background-color:#06DD06;
            }
            """)

    def setColorFailed(self, rackPos):
        self.square[rackPos].setStyleSheet("""
            QWidget
            {
                border-radius: 10px;
                background-color:#FC0B05;
            }
            """)

    def testTimeElapsed(self):
        if self.elapsedTimerStatus == True:
            self.sec = elapseTimer.elapsed() // 1000
            self.min = (self.sec // 60) % 60
            self.hour = self.sec // 3600
            self.sec = self.sec % 60
            self.testTime = '{:02d}:{:02d}:{:02d}'.format(self.hour, self.min, self.sec)
            self.lbl_time.setText(self.testTime)

    def setProgressBarDefault(self, rackPos):
        self.progressBar[rackPos].setMaximum(PBAR_VAL_100)
        self.progressBar[rackPos].setMinimum(PBAR_VAL_100)
        self.progressBar[rackPos].setValue(PBAR_VAL_0)

    def setProgressBarBusy(self, rackPos):
        self.progressBar[rackPos].setMaximum(PBAR_VAL_0)
        self.progressBar[rackPos].setMinimum(PBAR_VAL_0)
        self.progressBar[rackPos].setValue(PBAR_VAL_0)

    def setProgressBarDone(self, rackPos):
        self.progressBar[rackPos].setMaximum(PBAR_VAL_100)
        self.progressBar[rackPos].setMinimum(PBAR_VAL_0)
        self.progressBar[rackPos].setValue(PBAR_VAL_100)

    #==================== API ========================================
    def setProgressBar(self, rackPos, pbStatus):
        if pbStatus == PBarStatus.BUSY:
            self.setProgressBarBusy(rackPos)
        elif pbStatus == PBarStatus.DONE:
            self.setProgressBarDone(rackPos)
        else:
            self.setProgressBarDefault(rackPos)

    def setMacAddress(self, rackPos, macAddressValue):
        self.lbl_macAddressValue[rackPos].setText(macAddressValue)

    def setRackStatus(self, rackPos, rackStatus):
        if rackStatus == RackStatus.JOINED:
            self.setColorJoined(rackPos)
        elif rackStatus == RackStatus.PASSED:
            self.setColorPassed(rackPos)
        elif rackStatus == RackStatus.FAILED:
            self.setColorFailed(rackPos)
        else:
            self.setColorDefault(rackPos)

    def restartTestTime (self):
        elapseTimer.restart()
        self.elapsedTimerStatus = True

    def stopTestTime (self):
        self.elapsedTimerStatus = False

    #====================== Implement Control Logic here ======================
    #Tick handler (1 second by default) <Implement periodic task here>
    def tick(self):
        self.testTimeElapsed()

    #Slot which connected with Join Button and JoinAction <Implement Join task here>
    def joinNetwork(self):
        self.restartTestTime()

    #Slot which connected with Check Button and CheckAction <Implement Check task here>
    def checkCommunication(self):
        self.stopTestTime()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plcwidget = PLCGui()

    tickTimer = QTimer()
    tickTimer.timeout.connect(plcwidget.tick)
    tickTimer.start(TICK_PERIOD)

    elapseTimer = QElapsedTimer()
    elapseTimer.start()

    #=================Please remove this from real application=================
    #=================== Demonstration & example to use API ===================
    plcwidget.setMacAddress(RackPos.FIRST, '#############')

    plcwidget.setProgressBar(RackPos.FIRST, PBarStatus.BUSY)
    plcwidget.setProgressBar(RackPos.THIRD, PBarStatus.DONE)

    plcwidget.setRackStatus(RackPos.FIRST, RackStatus.DEFAULT)
    plcwidget.setRackStatus(RackPos.SECOND, RackStatus.JOINED)
    plcwidget.setRackStatus(RackPos.THIRD, RackStatus.PASSED)
    plcwidget.setRackStatus(RackPos.FOURTH, RackStatus.FAILED)
    #==========================================================================

    sys.exit(app.exec_())