class check:
    def numCheck(self, num):
        if int(num) <= 0 or int(num) > 26 or num[0] == "0":
            return False
        else:
            return True

    def numCorrect(self, board, num):
        for i in range(4):
            for j in range(4):
                if board[i][j] == num:
                    board[i][j] = str("O") #입력받은 수를 0로 바꿈
                else:
                    continue

        return board
                



            