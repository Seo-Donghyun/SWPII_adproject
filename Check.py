class check:
    def numCheck(self, num): # 입력된 숫자가 올바른 숫자인지 확인하는 함수
        if int(num) <= 0 or int(num) > 26 or num[0] == "0": # 숫자가 1 ~ 25가 아니라면, '4'가 아니라 '04' 같이 입력된다면
            return False
        else:
            return True

    def numCorrect(self, board, num): # 입력된 숫자가 빙고판에 있는 지 확인하는 함수
        for i in range(4):
            for j in range(4):
                if board[i][j] == num: # 만약 입력받은 수가 빙고판에 있다면
                    board[i][j] = str("O") # 빙고판에 해당 수를 0으로 바꿈
                else:
                    continue
        return board
                



            