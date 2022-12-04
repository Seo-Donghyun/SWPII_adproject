# 소프트웨어프로젝트2 7조 ad프로젝트
# 빙고게임

import sys
from PyQt5.QtCore import Qt # 가운데 정렬하기 위해 사용
from PyQt5.QtGui import QTextCursor # 텍스트 정렬시킬때 선택된 텍스트 해제시킬 때 사용
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLineEdit, QToolButton, QTextEdit, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QSizePolicy
from bingo import BingoCheck
from Check import check

class Button(QToolButton):

    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

class Bingogame(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.title = QLabel(self)  # 누구 차례입니다 출력
        font = self.title.font()
        font.setPointSize(20)
        self.title.setFont(font)

        self.numbutton = [x for x in range(0, 10)]

        for i in self.numbutton:  # 버튼 만들기 반복문
            self.numbutton[i] = Button(f'{i}', self.buttonClicked)
        self.bsbutton = Button('<-', self.buttonClicked)
        self.gobutton = Button('go!', self.buttonClicked)

        self.bingoboard = QTextEdit(self)  # 빙고판 보여줄 Textedit
        self.bingoboard.setReadOnly(True)
        font1 = self.bingoboard.font()
        font1.setPointSize(font1.pointSize() + 10)
        self.bingoboard.setFont(font1)
        self.bingoboard.setAlignment(Qt.AlignCenter)


        self.enterednum = QLineEdit(self)  # 입력한 숫자 보여줄 lineedit
        self.enterednum.setReadOnly(True)
        self.state = QLineEdit(self) # 입력한 숫자의 상태를 보여줌
        self.state.setReadOnly(True)
        self.writenum = QLineEdit(self)  # 지금 입력할 숫자를 보여줄 lineedit
        self.writenum.setReadOnly(True)

        hbox = QHBoxLayout() # 첫번째 줄("~~차례입니다." 출력)
        hbox1 = QHBoxLayout() # 두번째 줄(빙고판 출력)
        hbox2 = QHBoxLayout() # 세번째 줄(이미 입력한 숫자 출력)
        hbox3 = QHBoxLayout() # 네번째 줄(현재 상태 출력)
        hbox4 = QHBoxLayout() # 다섯번째 줄(지금 입력하는 숫자 출력)
        hbox5 = QHBoxLayout() # 여섯번째 줄(숫자 키패드 첫번째 줄)
        hbox6 = QHBoxLayout() # 일곱번째 줄(숫자 키패드 두번째 줄)
        vbox = QVBoxLayout()  # 위에 있는 hbox들을 모아서 vbox로 정렬

        hbox.addStretch(1)
        hbox.addWidget(self.title)
        hbox.addStretch(1)

        vbox.addLayout(hbox)

        hbox1.addStretch(1)
        hbox1.addWidget(self.bingoboard)
        hbox1.addStretch(1)

        vbox.addLayout(hbox1)

        hbox2.addStretch(1)
        hbox2.addWidget(self.enterednum)
        hbox2.addStretch(1)

        vbox.addLayout(hbox2)

        hbox3.addStretch(1)
        hbox3.addWidget(self.state)
        hbox3.addStretch(1)

        vbox.addLayout(hbox3)

        hbox4.addStretch(1)
        hbox4.addWidget(self.writenum)
        hbox4.addStretch(1)

        vbox.addLayout(hbox4)

        hbox5.addStretch(1)
        for i in range(1, 7):
            hbox5.addWidget(self.numbutton[i])
        hbox5.addStretch(1)

        vbox.addLayout(hbox5)

        hbox6.addStretch(1)
        for i in range(7, 10):
            hbox6.addWidget(self.numbutton[i])
        hbox6.addWidget(self.numbutton[0])
        hbox6.addWidget(self.bsbutton)
        hbox6.addWidget(self.gobutton)
        hbox6.addStretch(1)

        vbox.addLayout(hbox6)

        self.setLayout(vbox)


        self.setWindowTitle('Bingo game')
        self.move(300, 300)
        self.resize(300, 370)
        self.startgame()

    def buttonClicked(self): # 버튼 기능 구현
        button = self.sender()
        key = button.text()
        if key == '<-':
            result = self.writenum.text()
            result = result[:-1]
            self.writenum.setText(result)
        elif key == 'go!':
            self.gonumber()
        else:
            self.writenum.setText(self.writenum.text() + key)

    def startgame(self):
        self.bingo = BingoCheck()
        for i in range(2):
            self.bingo.board()
        self.title.setText(self.bingo.settitle())
        self.bingoboard.setText(self.bingo.showboard())
        self.bingoboard.selectAll()
        self.bingoboard.setAlignment(Qt.AlignCenter)
        self.bingoboard.moveCursor(QTextCursor.End)
        self.enterednum.setText(self.bingo.showusednum())
        self.writenum.clear()

    def gonumber(self):
        gonum = self.writenum.text()
        self.Check = check()
        self.writenum.clear()

        if len(gonum) == 0:
            self.state.setText("please write number")
            return self.state.text()

        if self.Check.numCheck(gonum) == False:
            self.state.setText("wrong number")
            return self.state.text()

        if gonum in self.bingo.usednum:
            self.state.setText("already used")
            return self.state.text()

        for i in range(2):
            self.bingo.boardlist[i] = self.Check.numCorrect(self.bingo.boardlist[i], gonum)

        if self.bingo.finish(self.bingo.whoturn() - 1) == True:
            self.bsbutton.setDisabled(True)
            self.gobutton.setDisabled(True)
            if self.bingo.finish(1 - (self.bingo.whoturn() - 1)) == True:
                self.bingoboard.clear()
                self.bingoboard.append(f"winner : " + " ".join(self.bingo.winplayer))
            else:
                self.bingoboard.clear()
                self.bingoboard.append(f"winner : " + " ".join(self.bingo.winplayer))

        else:
            if self.bingo.finish(1 - (self.bingo.whoturn() - 1)) == True:
                self.bingoboard.clear()
                self.bingoboard.append(f"winner : " + " ".join(self.bingo.winplayer))
            else:
                self.bingo.turnup()
                self.bingo.usednum.append(gonum)
                self.title.setText(self.bingo.settitle())
                self.bingoboard.setText(self.bingo.showboard())
                self.bingoboard.selectAll()
                self.bingoboard.setAlignment(Qt.AlignCenter)
                self.bingoboard.moveCursor(QTextCursor.End)
                self.enterednum.setText(self.bingo.showusednum())
                self.state.clear()
                return "again"


if __name__ == '__main__':
   app = QApplication(sys.argv)
   bi = Bingogame()
   bi.show()
   sys.exit(app.exec_())