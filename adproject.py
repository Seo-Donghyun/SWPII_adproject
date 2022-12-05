# 소프트웨어프로젝트2 7조 ad프로젝트
# 20223089 백운호, 20223091 서동현, 20223579 노민 에르덴
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
        font.setPointSize(20) # 글자 크기 설정
        self.title.setFont(font) # 글자 크기 적용

        self.numbutton = [x for x in range(0, 10)]

        for i in self.numbutton:  # 버튼 만들기 반복문
            self.numbutton[i] = Button(f'{i}', self.buttonClicked)
        self.bsbutton = Button('<-', self.buttonClicked)
        self.gobutton = Button('go!', self.buttonClicked)

        self.bingoboard = QTextEdit(self)  # 빙고판 보여줄 Textedit
        self.bingoboard.setReadOnly(True) # 읽기 모드로 전환
        font1 = self.bingoboard.font()
        font1.setPointSize(font1.pointSize() + 10) # 글자 크기 조정
        self.bingoboard.setFont(font1) # 적용
        self.bingoboard.setAlignment(Qt.AlignCenter) # 가운데 정렬


        self.enterednum = QLineEdit(self)  # 입력한 숫자 보여줄 lineedit
        self.enterednum.setReadOnly(True) # 읽기 모드로 전환
        self.enterednum.setFixedWidth(360)  # lineedit 너비 조정하는 메소드

        self.state = QLineEdit(self) # 입력한 숫자의 상태를 보여줌
        self.state.setReadOnly(True) # 읽기 모드로 전환

        self.writenum = QLineEdit(self)  # 지금 입력할 숫자를 보여줄 lineedit
        self.writenum.setReadOnly(True) # 읽기 모드로 전환

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
        for i in range(1, 7): # 숫자키 1 ~ 6
            hbox5.addWidget(self.numbutton[i])
        hbox5.addStretch(1)

        vbox.addLayout(hbox5)

        hbox6.addStretch(1)
        for i in range(7, 10): # 숫자키 7 ~ 9
            hbox6.addWidget(self.numbutton[i])
        hbox6.addWidget(self.numbutton[0]) # 숫자키 0
        hbox6.addWidget(self.bsbutton) # backspace 버튼
        hbox6.addWidget(self.gobutton) # go! 버튼
        hbox6.addStretch(1)

        vbox.addLayout(hbox6)

        self.setLayout(vbox)


        self.setWindowTitle('Bingo game') # 창 제목 설정
        self.move(300, 300) # 위치 조정
        self.resize(300, 370) # 창 크지 조정
        self.startgame() # 게임 스타트!!

    def buttonClicked(self): # 버튼 기능 구현
        button = self.sender()
        key = button.text() # 각 버튼 이름
        if key == '<-': # backspace 버튼을 누르면
            result = self.writenum.text() # 현재 입력되어있는 str 가져오고
            result = result[:-1] # 그 str의 마지막 글자를 빼고 다시 정의
            self.writenum.setText(result) # 마지막 글자를 뺀 str 다시 넣기
        elif key == 'go!': # go! 버튼을 누르면
            self.gonumber() # 아래의 go! 함수 적용
        else: # 그 외에 숫자키가 입력되면
            self.writenum.setText(self.writenum.text() + key) # 그 숫자를 입력

    def startgame(self): # 게임 시작했을 때 세팅
        self.bingo = BingoCheck() # BingoCheck 클래스의 인스턴스를 만듬
        for i in range(2): # 빙고판 2개 만들기
            self.bingo.board()
        self.title.setText(self.bingo.settitle()) # 제목 적용
        self.bingoboard.setText(self.bingo.showboard()) # 1p 빙고판 보여주기
        self.bingoboard.selectAll() # 입력한 빙고판을 선택해서
        self.bingoboard.setAlignment(Qt.AlignCenter) # 가운데 정렬
        self.bingoboard.moveCursor(QTextCursor.End) # 선택된 커서 제거
        self.enterednum.setText(self.bingo.showusednum()) # 입력한 숫자 보여주기(처음이라 아무것도 없음)
        self.writenum.clear() # 입력한 숫자 제거

    def gonumber(self): # 버튼 go!를 눌렀을 때 적용할 함수
        gonum = self.writenum.text() # 입력된 숫자를 저장
        self.Check = check() # check 클래스의 인스턴스 만듬
        self.writenum.clear() # 입력한 숫자 제거

        if len(gonum) == 0: # 만약 아무것도 입력을 안했다면
            self.state.setText("please write number") # 상태창에 메세지 출력
            return self.state.text()

        if self.Check.numCheck(gonum) == False: # 만약 입력한 숫자가 범위를 벗어나거나 잘못된 숫자이면
            self.state.setText("wrong number") # 상태창에 메세지 출력
            return self.state.text()

        if gonum in self.bingo.usednum: # 만약 입력한 숫자가 이미 입력한 숫자이면
            self.state.setText("already used") # 상태창에 메세지 출력
            return self.state.text()

        # 여기부터는 오류가 없으면 실행함
        for i in range(2):
            self.bingo.boardlist[i] = self.Check.numCorrect(self.bingo.boardlist[i], gonum) # 빙고판에 일치하는 숫자가 있는지 확인, 그리고 일치하면 0으로 바꿈

        if self.bingo.finish(self.bingo.whoturn() - 1) == True: # 만약 현재턴의 빙고판이 2빙고이상 이라면 -> 이긴 사람
            self.bsbutton.setDisabled(True) # 끝났지만 숫자를 입력해서 만들 버그를 생각해서 backspace, go! 버튼 비활성화
            self.gobutton.setDisabled(True)

            if self.bingo.finish(1 - (self.bingo.whoturn() - 1)) == True: # 만약 다른 사람의 빙고판이 동시에 2빙고이상이 된다면
                self.bingoboard.clear()
                self.bingoboard.append(f"winner : " + " ".join(self.bingo.winplayer)) # winner 출력
            else: # 다른 사람이 2빙고이상이 아니라면 -> 진 사람
                self.bingoboard.clear()
                self.bingoboard.append(f"winner : " + " ".join(self.bingo.winplayer)) # winner 출력

        else: # 만약 현재턴의 빙고판이 2빙고이상이 아니라면
            if self.bingo.finish(1 - (self.bingo.whoturn() - 1)) == True: # 그런데 다른 사람의 빙고판이 2빙고 이상이 됬다면 -> 게임을 이김
                self.bingoboard.clear()
                self.bingoboard.append(f"winner : " + " ".join(self.bingo.winplayer)) # winner 출력
            else: # 만약 둘 다 2빙고 이상이 아니라면 -> 게임이 안 끝남
                self.bingo.turnup() # 턴 수 증가
                self.bingo.usednum.append(gonum) # 사용한 숫자 추가
                self.title.setText(self.bingo.settitle()) # 여기서 부터는 startgame 과 동일
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