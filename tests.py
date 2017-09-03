import unittest
from movegenerator import *


class MyTestCase(unittest.TestCase):
    Board = [['0'] * 8 for i in range(8)]  # an 8 by 8 board
    def resetBoard(self):
        self.Board = [['0'] * 8 for i in range(8)]

    def assertMoves(self, moves, expectedMoves):
        ans = (len(moves) == expectedMoves)
        if not ans:
            return ans
        for i in range(len(moves)):
            ans = moves[i] in expectedMoves
            if not ans:
                return ans

        return ans

    def test_getColRow(self):
        col, row = getColAndRow('D4')
        self.assertEqual(col, 3)
        self.assertEqual(row, 3)
        try:
            col, row = getColAndRow('I9')
            self.assertTrue(False)
        except KeyError:
            self.assertTrue(True)

    def test_getPos(self):
        pos = getPos(3, 3)
        self.assertEqual(pos, 'D4'.lower())
        try:
            pos = getPos(8,8)
            self.assertTrue(False)
        except KeyError:
            self.assertTrue(True)

    def test_getmovesKnight(self):
        moves = getmovesKnight('D4', self.Board)
        expected_ans = ['b3', 'b5', 'f3', 'f5', 'c2', 'c6', 'e2', 'e6']
        self.assertEqual(moves, expected_ans)

        #Friendly obstruction
        col, row = getColAndRow('b3')
        self.Board[col][row] = 'WK'
        moves = getmovesKnight('D4', self.Board)
        expected_ans = ['b5', 'f3', 'f5', 'c2', 'c6', 'e2', 'e6']
        self.assertMoves(moves, expected_ans)

        #Enemy obstruction
        col, row = getColAndRow('b5')
        self.Board[col][row] = 'BK'
        moves = getmovesKnight('D4', self.Board)
        expected_ans = ['b5', 'f3', 'f5', 'c2', 'c6', 'e2', 'e6']
        self.assertMoves(moves, expected_ans)

        #Corners
        self.resetBoard()
        moves = getmovesKing('A1', self.Board)
        expected_ans = ['a2', 'b2', 'b1']
        self.assertMoves(moves, expected_ans)

    def test_getmovesRook(self):
        self.resetBoard()
        moves = getmovesRook('D4', self.Board)
        expected_ans = ['e4', 'f4', 'g4', 'h4', 'c4', 'b4', 'a4', 'd5', 'd6', 'd7', 'd8', 'd3', 'd2', 'd1']
        self.assertEqual(moves, expected_ans)

        #Horizontal check
        # Friendly obstruction
        col, row = getColAndRow('b3')
        self.Board[col][row] = 'WK'
        moves = getmovesRook('E4', self.Board)
        expected_ans = ['c4', 'b4', 'a4', 'd5', 'd6', 'd7', 'd8', 'd3', 'd2', 'd1']
        self.assertMoves(moves, expected_ans)

        # Enemy obstruction
        col, row = getColAndRow('b5')
        self.Board[col][row] = 'BK'
        moves = getmovesRook('B4', self.Board)
        expected_ans = ['b4', 'a4', 'd5', 'd6', 'd7', 'd8', 'd3', 'd2', 'd1']
        self.assertMoves(moves, expected_ans)

    def test_getmovesKing(self):
        self.resetBoard()
        moves = getmovesKing('D4', self.Board)
        expected_ans = ['d5', 'e5', 'e4', 'd3', 'c3', 'c4', 'e3', 'c5']
        self.assertEqual(moves, expected_ans)

        # Friendly obstruction
        col, row = getColAndRow('e4')
        self.Board[col][row] = 'WK'
        moves = getmovesKing('E4', self.Board)
        expected_ans = ['e5', 'f5', 'f4', 'e3', 'd3', 'd4', 'f3', 'd5']
        self.assertEqual(moves, expected_ans)

        # Enemy obstruction
        col, row = getColAndRow('b3')
        self.Board[col][row] = 'BK'
        moves = getmovesKing('E5', self.Board)
        expected_ans = ['e6', 'f6', 'f5', 'd4', 'd5', 'f4', 'd6']
        self.assertEqual(moves, expected_ans)

    def test_getmovesPawn(self):
        self.resetBoard()
        moves = getmovesPawn('D4', self.Board)
        expected_ans = ['d5']
        self.assertEqual(moves, expected_ans)

        #Friendly obstruction
        col, row = getColAndRow('D5')
        self.Board[col][row] = 'WK'
        moves = getmovesPawn('D4', self.Board)
        expected_ans = []
        self.assertEqual(moves, expected_ans)

        #Enemy obstruction
        self.resetBoard()
        col, row = getColAndRow('E5')
        self.Board[col][row] = 'BK'
        moves = getmovesPawn('D4', self.Board)
        expected_ans = ['d5', 'e5']
        self.assertEqual(moves, expected_ans)

    def test_getmovesBishop(self):
        self.resetBoard()
        moves = getmovesBishop('D4', self.Board)
        expected_ans = ['e5', 'c5', 'e3', 'c3', 'f6', 'b6', 'f2', 'b2', 'g7', 'a7', 'g1', 'a1', 'h8']
        self.assertEqual(moves, expected_ans)

        # Friendly obstruction
        col, row = getColAndRow('E5')
        self.Board[col][row] = 'WK'
        moves = getmovesBishop('D4', self.Board)
        expected_ans = ['c5', 'e3', 'c3', 'b6', 'f2', 'b2', 'a7', 'g1', 'a1']
        self.assertEqual(moves, expected_ans)

        # Enemy obstruction
        col, row = getColAndRow('E3')
        self.Board[col][row] = 'BK'
        moves = getmovesBishop('D4', self.Board)
        expected_ans = ['c5', 'e3', 'c3', 'b6', 'b2', 'a7', 'a1']
        self.assertEqual(moves, expected_ans)

    def test_getmovesQueen(self):
        self.resetBoard()
        moves = getmovesQueen('D4', self.Board)
        expected_ans = ['e4', 'f4', 'g4', 'h4', 'c4', 'b4', 'a4', 'd5', 'd6', 'd7', 'd8', 'd3', 'd2', 'd1', 'e5', 'c5', 'e3', 'c3', 'f6', 'b6', 'f2', 'b2', 'g7', 'a7', 'g1', 'a1', 'h8']
        self.assertEqual(moves, expected_ans)

        # Friendly obstruction
        col, row = getColAndRow('E5')
        self.Board[col][row] = 'WK'
        moves = getmovesQueen('D4', self.Board)
        expected_ans = ['e4', 'f4', 'g4', 'h4', 'c4', 'b4', 'a4', 'd5', 'd6', 'd7', 'd8', 'd3', 'd2', 'd1', 'c5', 'e3', 'c3', 'b6', 'f2', 'b2', 'a7', 'g1', 'a1']
        self.assertEqual(moves, expected_ans)

        # Enemy obstruction
        col, row = getColAndRow('E4')
        self.Board[col][row] = 'BK'
        moves = getmovesQueen('D4', self.Board)
        expected_ans = ['e4', 'c4', 'b4', 'a4', 'd5', 'd6', 'd7', 'd8', 'd3', 'd2', 'd1', 'c5', 'e3', 'c3', 'b6', 'f2', 'b2', 'a7', 'g1', 'a1']
        self.assertEqual(moves, expected_ans)

if __name__ == '__main__':
    unittest.main()
