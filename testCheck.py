import unittest

from Check import check
from bingo import BingoCheck

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.c1 = check()
        self.b1 = BingoCheck()

    def tearDown(self):
        pass

    def testNumCheck(self): # numCheck 테스트케이스 (1 ~ 25사이에 없거나 4를 04라고 적는 경우에 return False함)
        # 1. 올바른 숫자를 넣었을 때 return True 함
        self.assertTrue(self.c1.numCheck("17")) # 범위 안에 있으므로 return True
        self.assertTrue(self.c1.numCheck("1"))

        # 2. 범위 안에 있는 숫자가 아닐 때 return False 함
        self.assertFalse(self.c1.numCheck("30")) # 범위를 벗어나므로 return False
        self.assertFalse(self.c1.numCheck("0"))

        # 3. 4를 04라고 적는 경우 return False 함
        self.assertFalse(self.c1.numCheck("04")) # 잘못된 경우이므로 return False
        self.assertFalse(self.c1.numCheck("006"))

    def testNumCorrect(self): # numCorrect 테스트케이스 (숫자를 입력받으면 빙고판에서 일치하는 숫자를 "O"로 바꿈)
        # 먼저 2개의 빙고판 생성
        self.b1.boardlist = [[["1", "2", "3", "4"],
                             ["5", "6", "7", "8"],
                             ["9", "10", "11", "12"],
                             ["13", "14", "15", "16"]],
                             [["16", "15", "14", "13"],
                              ["12", "11", "10", "9"],
                              ["8", "7", "6", "5"],
                              ["4", "3", "2", "1"]]]

        # 1. 일치하는 숫자가 있는 경우 -> 그 자리에 "O"가 들어감
        for i in range(2):
            self.c1.numCorrect(self.b1.boardlist[i], "1") # 1을 입력했다고 가정

        self.assertEqual(self.b1.boardlist[0][0][0], "O") # 1이 있었던 자리에 "O"가 들어감
        self.assertEqual(self.b1.boardlist[1][3][3], "O")

        # 2. 일치하는 숫자가 없는 경우 -> 그대로
        self.prevboard1 = self.b1.boardlist[0] # 우선 숫자 입력하기전 빙고판을 다른 곳에 저장
        self.prevboard2 = self.b1.boardlist[1]

        for i in range(2):
            self.c1.numCorrect(self.b1.boardlist[i], "20") # 20을 입력했다고 가정

        self.assertEqual(self.prevboard1, self.b1.boardlist[0]) # 바뀐 게 없으므로, 이전 빙고판과 동일함
        self.assertEqual(self.prevboard2, self.b1.boardlist[1])

if __name__ == '__main__':
    unittest.main()
