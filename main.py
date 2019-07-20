'''
...Six Pieces Board Game...
This is a simple board game.
This game is made using PyQt5 GUI framework.
This is a single player game.

Author: Minul Hossain Tushar

email: minul2017hossain4@gmail.com
'''

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDesktopWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QIcon, QImage, QPalette, QBrush
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlaylist, QMediaPlayer
import random
from math import sqrt
from functools import partial
import sys


class Piece(QPushButton):
    def __init__(self):
        super().__init__()
        self.position = 0


class FirstWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()


    def initUi(self):

        self.boardSize = self.size()

        self.gmWin = gameWindow()
        self.creWin = CreditWindow()

        startBtn = QPushButton('New Game', self)
        startBtn.setGeometry(280, 220, 130, 50)
        startBtn.setFont(QFont('Arial', 15, QFont.Bold))
        startBtn.setStyleSheet('background-color: rgb(204, 204, 255)')
        startBtn.clicked.connect(self.openGameWindow)

        creditBtn = QPushButton('Credit', self)
        creditBtn.setGeometry(280, 300, 130, 50)
        creditBtn.setFont(QFont('Arial', 15, QFont.Bold))
        creditBtn.setStyleSheet('background-color: rgb(204, 204, 255)')
        creditBtn.clicked.connect(self.openCreditWindow)

        self.setWindowTitle('Frame animation')
        self.resize(700, 600)

        bgImage = QImage('images/firstpage')
        palette = QPalette()
        palette.setBrush(10, QBrush(bgImage))
        self.setPalette(palette)
        self.center()
        self.show()

    def openGameWindow(self):

        self.gmWin.show()
        self.close()

    def openCreditWindow(self):
        self.creWin.show()

    def center(self):

        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - self.boardSize.width()) / 2,
                  (screen.height() - self.boardSize.height()) / 2)



class CreditWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.boardSize = self.size()
        self.resize(700, 600)

        backBtn = QPushButton('Back', self)
        backBtn.move(300, 530)
        backBtn.setStyleSheet('background-color: rgb(204, 204, 255)')
        backBtn.setFont(QFont('Arial', 10, QFont.Bold))
        backBtn.clicked.connect(self.closeCredit)

        bgImage = QImage('images/credit.jpg')
        palette = QPalette()
        palette.setBrush(10, QBrush(bgImage))
        self.setPalette(palette)
        self.center()

    def closeCredit(self):
        self.close()

    def center(self):

        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - self.boardSize.width()) / 2,
                  (screen.height() - self.boardSize.height()) / 2)



class gameWindow(QWidget):      #main window

    def __init__(self):     #initialising
        super().__init__()

        self.initUi()


    def initUi(self):

        self.boardSize = self.size()        #for centering window


        self.pos = [(50, 100), (250, 100), (450, 100), (50, 300), (250, 300), (450, 300), (50, 500), (250, 500), (450, 500)]
        self.playerPieceClicked = [False, False, False]
        self.playerPieces = []
        self.botPieces = []
        self.clickBtns = []
        self.playerPiecePosition = [6, 7, 8]
        self.botPiecePosition = [0, 1, 2]
        self.startGameClicked = False
        self.playersTurn = bool(random.randint(0, 1))
        self.path = [(1, 3, 4), (0, 2, 4), (1, 4, 5), (0, 4, 6), (0, 1, 2, 3, 5, 6, 7, 8), (2, 4, 8), (3, 4, 7), (4, 6, 8), (4, 5, 7)]
        self.occupied = [True, True, True, False, False, False, True, True, True]
        self.playerScore = 0
        self.botScore = 0


        # Bot label
        self.botLabel = QLabel(self)
        self.botLabel.setText('Bot')
        self.botLabel.setGeometry(150, 30, 200, 30)
        self.botLabel.setStyleSheet('background-color: rgb(0, 143, 179)')
        self.botLabel.setFont(QFont('Arial', 15, QFont.Bold))
        self.botLabel.setAlignment(Qt.AlignCenter)

        # Player label
        self.playerLabel = QLabel(self)
        self.playerLabel.setText('You')
        self.playerLabel.setGeometry(150, 540, 200, 30)
        self.playerLabel.setStyleSheet('background-color: rgb(0, 143, 179)')
        self.playerLabel.setFont(QFont('Arial', 15, QFont.Bold))
        self.playerLabel.setAlignment(Qt.AlignCenter)
        if self.playersTurn:
            self.playerLabel.setStyleSheet('background-color: rgb(0, 153, 0)')
        else:
            self.botLabel.setStyleSheet('background-color: rgb(0, 153, 0)')

        # Player's Turn Label
        self.turnLabel = QLabel(self)
        self.turnLabel.setGeometry(530, 300, 200, 20)
        self.turnLabel.setFont(QFont('Arial', 15, QFont.Bold))
        if self.playersTurn:
            self.turnLabel.setText('Your turn !')
        else:
            self.turnLabel.setText("Bot's turn !")

        # Score Board for player and bot
        ScoreLabel = QLabel(self)
        ScoreLabel.setText('Score')
        ScoreLabel.setGeometry(530, 80, 70, 30)
        ScoreLabel.setFont(QFont('Arial', 15, QFont.Bold))
        ScoreLabel.setAlignment(Qt.AlignCenter)

        youLabel = QLabel(self)
        youLabel.setText('You :')
        youLabel.setGeometry(490, 120, 60, 30)
        youLabel.setFont(QFont('Arial', 15, QFont.Bold))
        youLabel.setAlignment(Qt.AlignCenter)

        botLabel = QLabel(self)
        botLabel.setText('Bot :')
        botLabel.setGeometry(490, 170, 60, 30)
        botLabel.setFont(QFont('Arial', 15, QFont.Bold))
        botLabel.setAlignment(Qt.AlignCenter)

        self.you = QLabel(self)
        self.you.setText('0')
        self.you.setGeometry(570, 120, 70, 30)
        self.you.setStyleSheet('background-color: rgb(122, 122, 82)')
        self.you.setFont(QFont('Arial', 15, QFont.Bold))
        self.you.setAlignment(Qt.AlignCenter)

        self.bot = QLabel(self)
        self.bot.setText('0')
        self.bot.setGeometry(570, 170, 70, 30)
        self.bot.setStyleSheet('background-color: rgb(122, 122, 82)')
        self.bot.setFont(QFont('Arial', 15, QFont.Bold))
        self.bot.setAlignment(Qt.AlignCenter)

        self.start = QPushButton('Start', self)
        self.start.setGeometry(530, 400, 100, 30)
        self.start.setFont(QFont('Arial', 15, QFont.Bold))
        self.start.setStyleSheet('background-color: rgb(204, 204, 255)')
        self.start.clicked.connect(self.startGame)

        self.moveBot = QPushButton(self)
        self.moveBot.setGeometry(580, 50, 1, 1)
        self.moveBot.setStyleSheet('background-color: rgb(204, 153, 255)')
        self.moveBot.clicked.connect(self.moveBotClicked)

        self.reset = QPushButton(self)
        self.reset.setGeometry(590, 50, 1, 1)
        self.reset.clicked.connect(self.resetGame)

        # Volume button
        self.is_volume_on = True
        self.volume = QPushButton(self)
        self.volume.setGeometry(550, 520, 25, 25)
        self.volume.setStyleSheet('background-color: rgb(204, 153, 255)')
        self.volume.setIcon(QIcon('images/volume_on.png'))
        self.volume.clicked.connect(self.volumeControl)


        # click points
        for i in range(9):
            clickBtn = QPushButton(self)
            self.clickPointEdit(clickBtn)
            self.centerButton(clickBtn, self.pos[i])
            clickBtn.clicked.connect(partial(self.clickPointAnim, i))
            self.clickBtns.append(clickBtn)


        # bot pieces
        for i in range(3):
            btn = QPushButton(self)
            btn.resize(30, 30)
            btn.setStyleSheet('background-color: rgb(89, 179, 0)')
            self.centerButton(btn, self.pos[i])
            self.botPieces.append(btn)


        # player's pieces
        for i in range(3):
            btn = QPushButton(self)
            btn.resize(30, 30)
            btn.setStyleSheet('background-color: rgb(230, 46, 0)')
            self.centerButton(btn, self.pos[i+6])
            btn.clicked.connect(partial(self.ppClicked, i))
            self.playerPieces.append(btn)


        # Music
        self.url = QUrl.fromLocalFile('musics/music.mp3')
        self.content = QMediaContent(self.url)
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(self.content)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.setVolume(10)
        self.player.play()


        #main window resizing
        self.setWindowTitle('Frame animation')
        self.resize(700, 600)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(204, 153, 255))
        self.setPalette(p)
        self.center()


    def startGame(self):
        if self.playersTurn == False and self.startGameClicked == False:
            self.botLogic()
            self.playersTurn = True
            self.changeGraphics()
        self.startGameClicked = True
        self.pieceClickSound()


    def moveBotClicked(self):

        if not self.playersTurn:
            self.botLogic()
            self.changeGraphics()

    def botLogic(self):

        pdist12 = self.distance(self.pos[self.playerPiecePosition[0]], self.pos[self.playerPiecePosition[1]])
        pdist23 = self.distance(self.pos[self.playerPiecePosition[1]], self.pos[self.playerPiecePosition[2]])
        pdist13 = self.distance(self.pos[self.playerPiecePosition[0]], self.pos[self.playerPiecePosition[2]])
        pdistance = [pdist12, pdist23, pdist13]

        bdist12 = self.distance(self.pos[self.botPiecePosition[0]], self.pos[self.botPiecePosition[1]])
        bdist23 = self.distance(self.pos[self.botPiecePosition[1]], self.pos[self.botPiecePosition[2]])
        bdist13 = self.distance(self.pos[self.botPiecePosition[0]], self.pos[self.botPiecePosition[2]])
        bdistance = [bdist12, bdist23, bdist13]

        dis56 = self.distance(self.pos[5], self.pos[6])
        dis57 = self.distance(self.pos[5], self.pos[7])

        self.a = True
        for i in range(3):
            for j in self.path[self.botPiecePosition[i]]:
                if not self.occupied[j]:
                    if sum(self.botPiecePosition) + j - self.botPiecePosition[i] == 12 and j % 2 == 0:
                        a1 = (self.playerPiecePosition[0], self.playerPiecePosition[1])
                        a2 = (self.playerPiecePosition[0], self.playerPiecePosition[2])
                        a3 = (self.playerPiecePosition[1], self.playerPiecePosition[2])
                        playersMoveList = [a1, a2, a3]
                        temp = True
                        for k in playersMoveList:
                            if k[0] + k[1] + self.botPiecePosition[i] == 12:
                                temp2 = -1
                                for n in self.playerPiecePosition:
                                    if n != k[0] and n != k[1]:
                                        temp2 = n
                                if self.botPiecePosition[i] in self.path[temp2]:
                                    x1 = self.pos[k[0]][0]
                                    y1 = self.pos[k[0]][1]
                                    x2 = self.pos[k[1]][0]
                                    y2 = self.pos[k[1]][1]
                                    x3 = self.pos[self.botPiecePosition[i]][0]
                                    y3 = self.pos[self.botPiecePosition[i]][1]
                                    if (x3 - x1) * (y2 - y1) - (x2 - x1) * (y3 - y1) == 0:
                                        temp = False
                        if temp:
                            self.a = False
                            self.doAnimation(self.botPieces[i], self.pos[self.botPiecePosition[i]], self.pos[j])
                            self.occupied[self.botPiecePosition[i]] = False
                            self.occupied[j] = True
                            self.botPiecePosition[i] = j


        if self.a:

            for i in range(3):
                for j in self.path[self.playerPiecePosition[i]]:
                    if not self.occupied[j]:
                        if sum(self.playerPiecePosition) - self.playerPiecePosition[i] + j == 12:
                            z1, z2 = -1, -1
                            for y in self.playerPiecePosition:
                                if y != self.playerPiecePosition[i]:
                                    z1 = y
                            for y in self.playerPiecePosition:
                                if y != self.playerPiecePosition[i] and y != z1:
                                    z2 = y

                            x1 = self.pos[z1][0]
                            y1 = self.pos[z1][1]
                            x2 = self.pos[z2][0]
                            y2 = self.pos[z2][1]
                            x3 = self.pos[j][0]
                            y3 = self.pos[j][1]
                            if (x3 - x1) * (y2 - y1) - (x2 - x1) * (y3 - y1) == 0:
                                #movePieceList = []
                                for ii in range(3):
                                    if j in self.path[self.botPiecePosition[ii]]:
                                        self.doAnimation(self.botPieces[ii], self.pos[self.botPiecePosition[ii]],
                                                         self.pos[j])
                                        self.occupied[self.botPiecePosition[ii]] = False
                                        self.occupied[j] = True
                                        self.botPiecePosition[ii] = j
                                        self.a = False


        if self.a:
            for i in range(3):
                for j in self.path[self.botPiecePosition[i]]:
                    if not self.occupied[j]:
                        if sum(self.botPiecePosition) + j - self.botPiecePosition[i] == 12:

                            a1 = (self.playerPiecePosition[0], self.playerPiecePosition[1])
                            a2 = (self.playerPiecePosition[0], self.playerPiecePosition[2])
                            a3 = (self.playerPiecePosition[1], self.playerPiecePosition[2])
                            playersMoveList = [a1, a2, a3]
                            temp = True
                            for k in playersMoveList:
                                if k[0] + k[1] + self.botPiecePosition[i] == 12:
                                    temp2 = -1
                                    for n in self.playerPiecePosition:
                                        if n != k[0] and n != k[1]:
                                            temp2 = n
                                    if self.botPiecePosition[i] in self.path[temp2]:
                                        x1 = self.pos[k[0]][0]
                                        y1 = self.pos[k[0]][1]
                                        x2 = self.pos[k[1]][0]
                                        y2 = self.pos[k[1]][1]
                                        x3 = self.pos[self.botPiecePosition[i]][0]
                                        y3 = self.pos[self.botPiecePosition[i]][1]
                                        if (x3 - x1) * (y2 - y1) - (x2 - x1) * (y3 - y1) == 0:
                                            temp = False
                            if temp:
                                self.doAnimation(self.botPieces[i], self.pos[self.botPiecePosition[i]], self.pos[j])
                                self.occupied[self.botPiecePosition[i]] = False
                                self.occupied[j] = True
                                self.botPiecePosition[i] = j
                                self.a = False


        if self.a and sum(self.playerPiecePosition) == 21 and sum(self.botPiecePosition) == 3:
            p = random.randint(0, 2)
            self.doAnimation(self.botPieces[p], self.pos[self.botPiecePosition[p]], self.pos[self.botPiecePosition[p] + 3])
            self.occupied[self.botPiecePosition[p]] = False
            self.occupied[p + 3] = True
            self.botPiecePosition[p] = p + 3
            self.a = False

        elif self.a and sum(self.botPiecePosition) == 3:
            if 200 in pdistance and dis56 in pdistance and dis57 in pdistance:
                movable = []
                for i in self.botPiecePosition:
                    if i + 3 not in self.playerPiecePosition:
                        movable.append(i)
                move = random.choice(movable)
                self.doAnimation(self.botPieces[move], self.pos[move], self.pos[move + 3])
                self.botPiecePosition[move] = move + 3
                self.occupied[move] = False
                self.occupied[move + 3] = True
                self.a = False

        elif self.a and 200 in pdistance and dis56 in pdistance and dis57 in pdistance and 7 in self.playerPiecePosition:
            if 200 in bdistance and dis56 in bdistance and dis57 in bdistance and 1 in self.botPiecePosition:
                for i in range(3):
                    if self.botPiecePosition[i] == 1:
                        self.doAnimation(self.botPieces[i], self.pos[1], self.pos[4])
                        self.botPiecePosition[i] = 4
                        self.occupied[1] = False
                        self.occupied[4] = True
                        self.a = False

            else:
                i = 0
                while i < 3:
                    if self.botPiecePosition[i] % 2 != 0:
                        break
                    i += 1
                if i == 3 and 4 in self.botPiecePosition:
                    for i in range(3):
                        for j in self.path[self.botPiecePosition[i]]:
                            if not self.occupied[j]:
                                if j - self.botPiecePosition[i] == 3:
                                    self.doAnimation(self.botPieces[i], self.pos[self.botPiecePosition[i]], self.pos[j])
                                    self.occupied[self.botPiecePosition[i]] = False
                                    self.occupied[j] = True
                                    self.botPiecePosition[i] = j
                                    self.a = False

        elif self.a and sum(self.botPiecePosition) == 12 and 4 in self.playerPiecePosition:
            if 200 in pdistance and dis57 in pdistance:
                notOccupied = []
                for i in range(9):
                    if self.occupied[i] == False:
                        notOccupied.append(i)
                movingPiece = -1
                movingPiecePosition = 0
                end = 0
                for i in range(3):
                    d = 0
                    for j in notOccupied:
                        if self.distance(self.pos[self.botPiecePosition[i]], self.pos[j]) > d:
                            d = self.distance(self.pos[self.botPiecePosition[i]], self.pos[j])
                    if d <= dis57:
                        movingPiece = i
                        movingPiecePosition = self.botPiecePosition[i]
                    if self.botPiecePosition[i] % 2 == 0:
                        end = 8 - self.botPiecePosition[i]
                if movingPiece > -1:
                    self.doAnimation(self.botPieces[movingPiece], self.pos[movingPiecePosition], self.pos[end])
                    self.occupied[movingPiecePosition] = False
                    self.occupied[end] = True
                    self.botPiecePosition[movingPiece] = end
                    self.a = False

        if self.a:
            moveList = []
            for i in range(3):
                for j in self.path[self.botPiecePosition[i]]:
                    if not self.occupied[j]:
                        a1 = (self.playerPiecePosition[0], self.playerPiecePosition[1])
                        a2 = (self.playerPiecePosition[0], self.playerPiecePosition[2])
                        a3 = (self.playerPiecePosition[1], self.playerPiecePosition[2])
                        playersMoveList = [a1, a2, a3]
                        temp = True
                        for k in playersMoveList:
                            if k[0] + k[1] + self.botPiecePosition[i] == 12:
                                temp2 = -1
                                for n in self.playerPiecePosition:
                                    if n != k[0] and n != k[1]:
                                        temp2 = n
                                if self.botPiecePosition[i] in self.path[temp2]:
                                    x1 = self.pos[k[0]][0]
                                    y1 = self.pos[k[0]][1]
                                    x2 = self.pos[k[1]][0]
                                    y2 = self.pos[k[1]][1]
                                    x3 = self.pos[self.botPiecePosition[i]][0]
                                    y3 = self.pos[self.botPiecePosition[i]][1]
                                    if (x3 - x1) * (y2 - y1) - (x2 - x1) * (y3 - y1) == 0:
                                        temp = False
                        if temp:
                            moveList.append((i, self.botPiecePosition[i], j))

            if len(moveList) == 0:
                for i in range(3):
                    for j in self.path[self.botPiecePosition[i]]:
                        if not self.occupied[j]:
                            moveList.append((i, self.botPiecePosition[i], j))

            move = random.choice(moveList)
            self.doAnimation(self.botPieces[move[0]], self.pos[move[1]], self.pos[move[2]])
            self.occupied[move[1]] = False
            self.occupied[move[2]] = True
            self.botPiecePosition[move[0]] = move[2]

        self.playersTurn = True



    def distance(self, p1, p2):
        return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    # if player's pieces are clicked, this method will be called
    def ppClicked(self, i):
        if self.playersTurn and self.startGameClicked:
            self.pieceClickSound()

            self.playerPieces[i].resize(40, 40)
            for j in range(3):
                if j != i:
                    self.playerPieces[j].resize(30, 30)

            self.playerPieceClicked[i] = True
            for j in range(3):
                if j != i:
                    self.playerPieceClicked[j] = False

    def paintEvent(self, QPaintEvent):

        painter = QPainter()
        painter.begin(self)
        self.drawBoard(painter)
        painter.end()

    def drawBoard(self, painter):
        painter.setPen(QPen(QColor(153, 0, 255), 10))
        painter.drawRect(50, 100, 400, 400)
        painter.drawLine(52, 102, 448, 498)
        painter.drawLine(448, 102, 52, 498)
        painter.drawLine(250, 100, 250, 500)
        painter.drawLine(50, 300, 450, 300)


    def center(self):

        screen = QDesktopWidget().screenGeometry()
        self.move(screen.width() / 2 - self.boardSize.width() / 2,
                  screen.height() / 2 - self.boardSize.height() / 2)


    def centerButton(self, button, point):

        size = button.size()
        button.move(point[0] - size.width() / 2, point[1] - size.height() / 2)


    def clickPointEdit(self, clickPoint):

        clickPoint.resize(20, 20)
        clickPoint.setStyleSheet('background-color: rgb(153, 0, 255)')


    def volumeControl(self):

        if self.is_volume_on:
            self.player.pause()
            self.volume.setIcon(QIcon('volume_off'))
            self.is_volume_on = False

        else:
            self.player.play()
            self.volume.setIcon(QIcon('volume_on'))
            self.is_volume_on = True


    def pieceClickSound(self):

        self.url2 = QUrl.fromLocalFile('musics/pieceClickSound.mp3')
        self.content2 = QMediaContent(self.url2)

        self.player2 = QMediaPlayer()
        self.player2.setMedia(self.content2)
        self.player2.play()


    def funnySound(self):

        self.url4 = QUrl.fromLocalFile('musics/funnySound.mp3')
        self.content4 = QMediaContent(self.url4)

        self.player4 = QMediaPlayer()
        self.player4.setMedia(self.content4)
        self.player4.play()

    def winSound(self):

        self.url3 = QUrl.fromLocalFile('musics/winSoundEfect.mp3')
        self.content3 = QMediaContent(self.url3)

        self.player3 = QMediaPlayer()
        self.player3.setMedia(self.content3)
        self.player3.play()

    def resetGame(self):

        for i in range(3):
            self.centerButton(self.playerPieces[i], self.pos[i + 6])
            self.centerButton(self.botPieces[i], self.pos[i])
            self.playerPieces[i].setStyleSheet('background-color: rgb(230, 46, 0)')
            self.botPieces[i].setStyleSheet('background-color: rgb(89, 179, 0)')

        self.botPiecePosition = [0, 1, 2]
        self.playerPiecePosition = [6, 7, 8]
        self.occupied = [True, True, True, False, False, False, True, True, True]
        self.playersTurn = random.choice([True, False])
        if self.playersTurn:
            self.turnLabel.setText('Your turn !')
            self.playerLabel.setStyleSheet('background-color: rgb(0, 153, 0)')
            self.botLabel.setStyleSheet('background-color: rgb(0, 143, 179)')
        else:
            self.turnLabel.setText("Bot's turn !")
            self.playerLabel.setStyleSheet('background-color: rgb(0, 143, 179)')
            self.botLabel.setStyleSheet('background-color: rgb(0, 153, 0)')
        self.start.animateClick(2500)

    def changeGraphics(self):

        if self.playersTurn:
            if sum(self.botPiecePosition) == 12:
                x1 = self.pos[self.botPiecePosition[0]][0]
                y1 = self.pos[self.botPiecePosition[0]][1]
                x2 = self.pos[self.botPiecePosition[1]][0]
                y2 = self.pos[self.botPiecePosition[1]][1]
                x3 = self.pos[self.botPiecePosition[2]][0]
                y3 = self.pos[self.botPiecePosition[2]][1]
                if (x3 - x1)*(y2 - y1) - (x2 - x1)*(y3 - y1) == 0:
                    for i in self.botPieces:
                        i.setStyleSheet('background-color: rgb(0, 102, 255)')
                    self.botScore += 1
                    self.bot.setText(str(self.botScore))
                    self.startGameClicked = False
                    self.turnLabel.setText('Bot wins !!')
                    self.winSound()
                    self.reset.animateClick(5000)
            else:
                self.turnLabel.setText("Your turn !")
                self.playerLabel.setStyleSheet('background-color: rgb(0, 153, 0)')
                self.botLabel.setStyleSheet('background-color: rgb(0, 143, 179)')
        else:
            if sum(self.playerPiecePosition) == 12:
                x1 = self.pos[self.playerPiecePosition[0]][0]
                y1 = self.pos[self.playerPiecePosition[0]][1]
                x2 = self.pos[self.playerPiecePosition[1]][0]
                y2 = self.pos[self.playerPiecePosition[1]][1]
                x3 = self.pos[self.playerPiecePosition[2]][0]
                y3 = self.pos[self.playerPiecePosition[2]][1]
                if (x3 - x1) * (y2 - y1) - (x2 - x1) * (y3 - y1) == 0:
                    for i in self.playerPieces:
                        i.setStyleSheet('background-color: rgb(0, 102, 255)')
                    self.playerScore += 1
                    self.you.setText(str(self.playerScore))
                    self.startGameClicked = False
                    self.turnLabel.setText('You win !!')
                    self.winSound()
                    self.reset.animateClick(4500)
            else:
                self.turnLabel.setText("Bot's turn !")
                self.playerLabel.setStyleSheet('background-color: rgb(0, 143, 179)')
                self.botLabel.setStyleSheet('background-color: rgb(0, 153, 0)')

    #new
    def clickPointAnim(self, i):

        for j in range(3):
            if self.playerPieceClicked[j]:
                if i == 0:
                    if self.playerPiecePosition[j] == 1 or self.playerPiecePosition[j] == 4 or self.playerPiecePosition[j] == 3:
                        self.doAnimation(self.playerPieces[j], self.pos[self.playerPiecePosition[j]], self.pos[i])
                        self.tttt(i, j)
                    else:
                        self.funnySound()
                elif i == 1:
                    if self.playerPiecePosition[j] == 0 or self.playerPiecePosition[j] == 4 or self.playerPiecePosition[j] == 2:
                        self.doAnimation(self.playerPieces[j], self.pos[self.playerPiecePosition[j]], self.pos[i])
                        self.tttt(i, j)
                    else:
                        self.funnySound()
                elif i == 2:
                    if self.playerPiecePosition[j] == 1 or self.playerPiecePosition[j] == 4 or self.playerPiecePosition[j] == 5:
                        self.doAnimation(self.playerPieces[j], self.pos[self.playerPiecePosition[j]], self.pos[i])
                        self.tttt(i, j)
                    else:
                        self.funnySound()
                elif i == 3:
                    if self.playerPiecePosition[j] == 0 or self.playerPiecePosition[j] == 4 or self.playerPiecePosition[j] == 6:
                        self.doAnimation(self.playerPieces[j], self.pos[self.playerPiecePosition[j]], self.pos[i])
                        self.tttt(i, j)
                    else:
                        self.funnySound()
                elif i == 4:
                    self.doAnimation(self.playerPieces[j], self.pos[self.playerPiecePosition[j]], self.pos[i])
                    self.tttt(i, j)
                elif i == 5:
                    if self.playerPiecePosition[j] == 2 or self.playerPiecePosition[j] == 4 or self.playerPiecePosition[j] == 8:
                        self.doAnimation(self.playerPieces[j], self.pos[self.playerPiecePosition[j]], self.pos[i])
                        self.tttt(i, j)
                    else:
                        self.funnySound()
                elif i == 6:
                    if self.playerPiecePosition[j] == 3 or self.playerPiecePosition[j] == 4 or self.playerPiecePosition[j] == 7:
                        self.doAnimation(self.playerPieces[j], self.pos[self.playerPiecePosition[j]], self.pos[i])
                        self.tttt(i, j)
                    else:
                        self.funnySound()
                elif i == 7:
                    if self.playerPiecePosition[j] == 6 or self.playerPiecePosition[j] == 4 or self.playerPiecePosition[j] == 8:
                        self.doAnimation(self.playerPieces[j], self.pos[self.playerPiecePosition[j]], self.pos[i])
                        self.tttt(i, j)
                    else:
                        self.funnySound()
                else:
                    if self.playerPiecePosition[j] == 5 or self.playerPiecePosition[j] == 4 or self.playerPiecePosition[j] == 7:
                        self.doAnimation(self.playerPieces[j], self.pos[self.playerPiecePosition[j]], self.pos[i])
                        self.tttt(i, j)
                    else:
                        self.funnySound()


    def tttt(self, i, j):

        self.occupied[self.playerPiecePosition[j]] = False
        self.occupied[i] = True
        self.playerPiecePosition[j] = i
        self.playerPieceClicked[j] = False
        self.playersTurn = False
        self.changeGraphics()
        x1 = self.pos[self.playerPiecePosition[0]][0]
        y1 = self.pos[self.playerPiecePosition[0]][1]
        x2 = self.pos[self.playerPiecePosition[1]][0]
        y2 = self.pos[self.playerPiecePosition[1]][1]
        x3 = self.pos[self.playerPiecePosition[2]][0]
        y3 = self.pos[self.playerPiecePosition[2]][1]
        if not (sum(self.playerPiecePosition) == 12 and (x3 - x1) * (y2 - y1) - (x2 - x1) * (y3 - y1) == 0):
            self.moveBot.animateClick(1000)


    def doAnimation(self, piece, start, end):


        self.url3 = QUrl.fromLocalFile('musics/pieceMovingSound.mp3')
        self.content3 = QMediaContent(self.url3)

        self.player3 = QMediaPlayer()
        self.player3.setMedia(self.content3)
        self.player3.play()

        self.anim = QPropertyAnimation(piece, b"geometry")
        self.anim.setDuration(600)
        self.anim.setStartValue(QRect(start[0] - 15, start[1] - 15, 30, 30))
        self.anim.setEndValue(QRect(end[0] - 15, end[1] - 15, 30, 30))
        self.anim.start()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = FirstWindow()
    sys.exit(app.exec_())
