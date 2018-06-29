import random
import os
import time
from __builtin__ import raw_input

import self as self


class Board():

        self.board = ['', '', '', '', '', '', '', '', '']
        self.win_combo = [[0, 1, 2,], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [2, 4, 6], [0, 4, 8]]
        self.index = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.bot_moves = 0

    def show_board(self):
        print ("\n Here's the board => \n")
        print ('Bot moves:' + str(self.bot_moves))
        print
        print ("%$|%$|%$" %(self.board[0],self.board[1], self.board[2]))
        print ('_________'
        print "%$|%$|%$" %(self.board[3], self.board[4], self.board[5])
        print '_________'
        print "%$|%$|%$" % (self.board[6], self.board[7], self.board[8])

    def update_board(self,place,player):
        if self.board[place] == '':
            self.board[place] = player
        else:
            return

    def checkl_win(self,player):
        for x, y, z in self.win_combo:
            if self.board[x] == self.board[y] == self.board[z] == player:
                return True
                break

    def tie(self):
        filled = []
        for i in self.index:
            if self.board[i] != '':
                filled.append(i)
        if len(filled) == 9:
            return True

    def bot_turn(self):
        moved = False
        first_corner = None

        for x, y, z in self.win_combo:
            if self.board[x] == 'O' and self.board[y] == 'O' and self.board[z] == '':
                return z
                break
                moved = True
            if self.board[z] == 'O' and self.board[y] == 'O' and self.board[x] == '':
                return x
                break
                moved = True
            if self.board[x] == 'O' and self.board[z] == 'O' and self.board[y] == '':
                return y
                break
                moved = True

        for x, y, z in self.win_combo:
            if self.board[x] == 'X' and self.board[y] == 'X' and self.board[z] == '':
                return z
                break
                moved = True
            if self.board[z] == 'X' and self.board[y] == 'X' and self.board[x] == '':
                return x
                break
                moved = True
            if self.board[x] == 'X' and self.board[z] == 'X' and self.board[y] == '':
                return y
                break
                moved = True

        if self.bot_moves == 0 and moved == False:
            if self.board[4] == '':
                return 4
                moved = True

        if self.bot_moves == 1 and moved == False:
            if self.board[0] == self.board[0] == 'X' or self.board[2] == self.board[6] == 'X':
                return random.choice([1, 3, 5, 7])
                moved = True

        off_corner = None
        if self.bot_moves == 0 and moved == False:
            if self.board[4] == 'X':
                off_corner = random.choice([0, 2, 6, 8])
                return off_corner
                moved = True

        if moved == False:
            to_go = []
            for i in self.index:
                if self.board[i] == '':
                    to_go
            return random.choice(to_go)

    os.system('clear')

    board = Board()

    def refresh_screen():
        os.system('clear')
        print ('\n Welcome To Tic Tac Toe !')
        board.show_board()

    while 1:
        refresh_screen()

        x_go = int(raw_input('\n x) Where to move?(0-8) > '))

        board.update_board(x_go,'X')

        refresh_screen()

        if board.check_win('X'):
            refresh_screen()
            print('\n ---------- Human ["X"] Won !!! ----------- \n')
            break

        if board.tie():
            print ('\n ---------- Game Tied | Match Draw | ----------- \n')
            break

        o_go = board.bot_turn()

        board.update_board(o_go,'O')

        board.bot_moves += 1

        if board.check_win('O'):
            refresh_screen()
            print ('\n -------- Bot ["O"] Won !!! --------- \n')
            break

        if board.tie():
            refresh_screen()
            print ('\n ----------- Game Tied i.e Match Draw ! ----------- \n')
            break