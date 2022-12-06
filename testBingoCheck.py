import unittest

from bingo import BingoCheck

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.b1 = BingoCheck()

    def tearDown(self):
        pass

    def testBoard(self): # board 테스트케이스 (빙고판 만듬)
        self.num1 = set() # 빙고판의 숫자를 넣을 세트(중복을 허용하지 않으므로, 정상적이라면 len이 16이여야 함)
        self.num2 = set()

        # 1. 두 빙고판이 같은 경우가 있는지
        for i in range(2):
            self.b1.board()
        self.assertNotEqual(self.b1.boardlist[0], self.b1.boardlist[1]) # 두 빙고판은 다르므로 assertNotEqual로 비교함

        # 2. 각 빙고판에 중복된 숫자가 있는지
        for i in self.b1.boardlist[0]: # 빙고판에 있는 모든 숫자를 위에서 정의한 set에 넣음
            for j in i:
                self.num1.add(j)

        for i in self.b1.boardlist[1]:
            for j in i:
                self.num2.add(j)

        self.assertEqual(len(self.num1), 16) # 중복되는 숫자가 없으므로, len(num1) = len(num2) = 16이여야 합니다.
        self.assertEqual(len(self.num2), 16)

    def testShowBoard(self): # showboard 테스트케이스 (빙고판을 보기 쉽게 return함)
        # 위의 메소드에 의해 만들어지는 것 처럼 중복 숫자가 없고, 다른 두 개의 빙고판을 정의
        self.b1.boardlist = [[["1", "2", "3", "4"],
                              ["5", "6", "7", "8"],
                              ["9", "10", "11", "12"],
                              ["13", "14", "15", "16"]],
                             [["16", "15", "14", "13"],
                              ["12", "11", "10", "9"],
                              ["8", "7", "6", "5"],
                              ["4", "3", "2", "1"]]]

        # showboard의 return 값을 테스트할 문자열
        self.sbtestcase1 = """1  2  3  4
5  6  7  8
9  10  11  12
13  14  15  16
"""

        self.sbtestcase2 = """16  15  14  13
12  11  10  9
8  7  6  5
4  3  2  1
"""

        self.b1.turn = 0 # 테스트하기 위해 bingo 객체의 turn을 0으로 정의
        self.assertEqual(self.sbtestcase1, self.b1.showboard())
        self.b1.turn = 1 # 테스트하기 위해 bingo 객체의 turn을 1로 정의
        self.assertEqual(self.sbtestcase2, self.b1.showboard())

    def testWhoTurn(self): # whoturn 테스트케이스 (누구 턴인지 숫자로 return)
        # 1p는 1, 2p는 2를 return 함
        self.b1.turn = 0 # 위에서 잠깐 사용했던 관계로 다시 0으로 초기화
        self.assertEqual(self.b1.whoturn(), 1) # 초기상태(1p 차례일 때) 1을 return 함

        self.b1.turn = 1 # 다음 턴으로 넘어간다면
        self.assertEqual(self.b1.whoturn(), 2) # 2p 차례일 때, 2를 return 함

    def testSetTitle(self): # settitle 테스트케이스 (gui위에 누구 차례인지 표시하는 문자열을 return)
        self.b1.turn = 0  # 위에서 사용했던 관계로 다시 0으로 초기화
        self.assertEqual(self.b1.settitle(), "1p 차례입니다.") # 처음에는 1p 차례

        self.b1.turn = 1
        self.assertEqual(self.b1.settitle(), "2p 차례입니다.") # 다음 턴에는 2p 차례

    def testTurnUp(self): # turnup 테스트케이스 (다음 턴으로 넘어갈 때 turn += 1을 하고 return)
        self.b1.turn = 0  # 위에서 사용했던 관계로 다시 0으로 초기화
        self.b1.turnup() # 다음 턴으로 넘어갔을 때
        self.assertEqual(self.b1.turn, 1) # turn은 1로 증가
        self.b1.turnup() # 다시 다음 턴으로 넘어갔을 때
        self.assertEqual(self.b1.turn, 2) # turn은 2로 증가

    def testShowUsednum(self): # showusednum 테스트케이스 (이미 사용한 숫자를 저장한 리스트의 원소들을 공백을 기준으로 return)
        self.b1.usednum = ["4", "6", "10"] # 예시
        self.assertEqual("4 6 10", self.b1.showusednum()) # 리스트의 원소를 공백을 기준으로 return함

    def testFinish(self): # finish 테스트케이스 (2빙고이상이 되었는 지 판단)
        # 1. 둘 다 2빙고 이상이 아닐 때
        self.b1.boardlist = [[["1", "2", "3", "4"],
                              ["5", "6", "7", "8"],
                              ["9", "10", "11", "12"],
                              ["13", "14", "15", "16"]],
                             [["16", "15", "14", "13"],
                              ["12", "11", "10", "9"],
                              ["8", "7", "6", "5"],
                              ["4", "3", "2", "1"]]]
        self.assertFalse(self.b1.finish(0)) # 아무것도 입력이 되지 않은 상태이므로 2빙고이상이 아님
        self.assertFalse(self.b1.finish(1))
        self.assertNotIn("1p", self.b1.winplayer) # 둘 다 2빙고 이상이 아니므로 winplayer에 아직 아무것도 없음
        self.assertNotIn("2p", self.b1.winplayer)

        # 2. 1p만 2빙고 이상일 때
        self.b1.boardlist[0] = [["O", "O", "O", "O"], # 2빙고인 상황으로 가정함
                              ["O", "6", "7", "8"],
                              ["O", "10", "11", "12"],
                              ["O", "14", "15", "16"]]

        self.assertTrue(self.b1.finish(0)) # 1p는 2빙고이므로 return True, 이긴 사람을 넣는 리스트에 추가
        self.assertFalse(self.b1.finish(1)) # 2p는 아직 2빙고가 아님
        self.assertIn("1p", self.b1.winplayer)
        self.assertNotIn("2p", self.b1.winplayer)

        self.b1.winplayer = [] # 다른 경우에도 테스트해야하므로 다서 초기 상태로

        # 3. 2p만 2빙고 이상일 때
        self.b1.boardlist = [[["1", "2", "3", "4"], # 2p만 2빙고이상인 경우로 가정
                              ["5", "6", "7", "8"],
                              ["9", "10", "11", "12"],
                              ["13", "14", "15", "16"]],
                             [["O", "15", "14", "O"],
                              ["12", "O", "O", "9"],
                              ["8", "O", "O", "5"],
                              ["O", "3", "2", "O"]]]

        self.assertFalse(self.b1.finish(0))  # 1p는 아직 2빙고가 아님
        self.assertTrue(self.b1.finish(1))  # 2p는 2빙고이므로 return True, 이긴 사람을 넣는 리스트에 추가
        self.assertNotIn("1p", self.b1.winplayer)
        self.assertIn("2p", self.b1.winplayer)

        self.b1.winplayer = []  # 다른 경우에도 테스트해야하므로 다서 초기 상태로

        # 4. 1p, 2p 둘 다 2빙고 이상일 때
        self.b1.boardlist = [[["O", "O", "O", "O"],  # 1p, 2p 둘 다 2빙고이상인 경우로 가정
                              ["O", "6", "7", "8"],
                              ["O", "10", "11", "12"],
                              ["O", "14", "15", "16"]],
                             [["O", "15", "14", "O"],
                              ["12", "O", "O", "9"],
                              ["8", "O", "O", "5"],
                              ["O", "3", "2", "O"]]]

        self.assertTrue(self.b1.finish(0))  # 1p는 2빙고이므로 return True, 이긴 사람을 넣는 리스트에 추가
        self.assertTrue(self.b1.finish(1))  # 2p는 2빙고이므로 return True, 이긴 사람을 넣는 리스트에 추가
        self.assertIn("1p", self.b1.winplayer)
        self.assertIn("2p", self.b1.winplayer)


if __name__ == '__main__':
    unittest.main()
