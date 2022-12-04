import numpy as np

class BingoCheck:
    def __init__(self):
        self.bingo = 0
        self.board_ = [[0 for i in range(4)] for j in range(4)]
        self.boardlist = []
        self.turn = 0
        self.usednum = []
        self.winplayer = []

    def board(self):  # 중복 없이 빙고판 생성
        list_ = np.random.choice(range(1, 25), 16, replace=False)
        idx = 0
        for i in range(4):
            for j in range(4):
                self.board_[i][j] = str(list_[idx])
                idx += 1
        for a in self.board_:
            print(a)
        print('')
        self.boardlist.append(self.board_)
        self.board_ = [[0 for i in range(4)] for j in range(4)]

    def showboard(self):
        display = ""
        for i in self.boardlist[self.whoturn() - 1]:
            display += "  ".join(i) + '\n'
        return display

    def whoturn(self):
        return self.turn % 2 + 1
    # 1p는 turn이 1, 2p는 turn이 2

    def settitle(self):
        return f"{self.whoturn()}p 차례입니다."

    def turnup(self):
        self.turn += 1

    def showusednum(self):
        return " ".join(self.usednum)


    def finish(self, index):

        a = self.boardlist[index]

        for i in range(4):  # 가로
            for j in range(4):
                if a[i][j] == str("O"):
                    continue
                else:
                    break
            else:
                self.bingo += 1

        for i in range(4):  # 세로
            for j in range(4):
                if a[j][i] == str("O"):
                    continue
                else:
                    break
            else:
                self.bingo += 1

        for i in range(4):  # 대각선
            if a[i][i] == str(0):
                continue
            else:
                break
        else:
            self.bingo += 1

        for i in range(4):  # 대각선
            if a[3 - i][i] == str("O"):
                continue
            else:
                break
        else:
            self.bingo += 1

        if self.bingo != 2:
            self.bingo = 0
            return False

        elif self.bingo == 2:
            self.winplayer.append(str(index + 1) + "p")
            self.bingo = 0
            return True
