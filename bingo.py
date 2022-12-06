# 소프트웨어프로젝트2 7조 ad프로젝트
# 20223089 백운호, 20223091 서동현, 20223579 노민 에르덴
# 빙고게임

import numpy as np

class BingoCheck:
    def __init__(self):
        self.bingo = 0 # 빙고 수 판단
        self.board_ = [[0 for i in range(4)] for j in range(4)] # 빙고판 기본 상태
        self.boardlist = [] # 2 사람의 빙고판을 저장할 리스트
        self.turn = 0 # 턴 수
        self.usednum = [] # 사용한 숫자를 저장할 리스트
        self.winplayer = [] # 이긴 사람

    def board(self):  # 중복 없이 빙고판 생성
        list_ = np.random.choice(range(1, 25), 16, replace=False) # 무작위로 중복을 허용하지 않고 1 ~ 25중에서 16개의 숫자를 뽑음
        idx = 0 # 무작위로 뽑힌 숫자가 있는 list_의 인덱스
        for i in range(4):
            for j in range(4):
                self.board_[i][j] = str(list_[idx]) # 빙고판 하나씩 숫자 넣음(str형태로)
                idx += 1
        for a in self.board_: # 여기는 테스트 할 때 빙고판을 볼 수 있도록 만든 코드
            print(a)
        print('')
        self.boardlist.append(self.board_) # 만들어진 빙고판을 boardlist에 저장
        self.board_ = [[0 for i in range(4)] for j in range(4)] # 빙고판의 기본상태로 다시 돌림

    def showboard(self): # 빙고판 보여주기
        display = ""
        for i in self.boardlist[self.whoturn() - 1]:
            display += "  ".join(i) + '\n' # 빙고판의 한 줄씩 가져와서 숫자들을 공백을 기준점으로 만듬, 출력할 때 개행문자 적용
        return display

    def whoturn(self): # 누구 턴인지 계산
        return self.turn % 2 + 1
    # 1p는 turn이 1, 2p는 turn이 2

    def settitle(self): # 제목에 "누구 차례입니다."를 return하는 함수
        return f"{self.whoturn()}p 차례입니다."

    def turnup(self): # go!를 눌렀을 때 턴 수 증가
        self.turn += 1

    def showusednum(self): # 사용한 숫자를 출력
        return " ".join(self.usednum)


    def finish(self, index): # 빙고판이 2빙고이상인지 확인

        a = self.boardlist[index]

        for i in range(4):  # 가로
            for j in range(4):
                if a[i][j] == str("O"):
                    continue
                else:
                    break
            else: # 만약 가로 한 줄이 전부 "O"라면, 빙고이므로
                self.bingo += 1 # 빙고 수 증가

        for i in range(4):  # 세로
            for j in range(4):
                if a[j][i] == str("O"):
                    continue
                else:
                    break
            else: # 만약 세로 한 줄이 전부 "O"라면, 빙고이므로
                self.bingo += 1 # 빙고 수 증가

        for i in range(4):  # 대각선(왼쪽 위 ~ 오른쪽 아래)
            if a[i][i] == str("O"):
                continue
            else:
                break
        else: # 만약 대각선 한 줄이 전부 "O"라면, 빙고이므로
            self.bingo += 1 # 빙고 수 증가

        for i in range(4):  # 대각선
            if a[3 - i][i] == str("O"):
                continue
            else:
                break
        else: # 만약 대각선 한 줄이 전부 "O"라면, 빙고이므로
            self.bingo += 1 # 빙고 수 증가

        if self.bingo >= 2: # 2빙고 이상이라면 -> 이겼다
            self.winplayer.append(str(index + 1) + "p") # 해당 사람을 winplayer에 넣고
            self.bingo = 0 # 다른 사람의 빙고판을 확인하기 위해 빙고 수를 0으로 바꿈
            return True

        elif self.bingo < 2: # 2빙고이상이 아니라면
            self.bingo = 0 # 다른 사람의 빙고판을 확인하기 위해 빙고 수를 0으로 바꿈
            return False
