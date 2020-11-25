import gi
import random

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Game

class Board:
	def __init__(self, size):
		self.size = size;
		board = [[0 for i in range(size)] for j in range(size)]
		for i in range(size):
			for j in range(size):
				x = random.uniform(0,1)
				if (x >= 10/64):
					board[i][j] = 0 # no mine
					print("0", end=" ")
				else:
					board[i][j] = 10 # mine
					print("X", end=" ")

			print()
		print()
		for i in range(size):
			for j in range(size):
				if (board[i][j] == 0):
					if (i > 0 and j > 0):
						if (board[i-1][j-1] == 10):
							board[i][j]+= 1

					if (j > 0):
						if (board[i][j-1] == 10):
							board[i][j]+= 1

					if (i < size-1 and j > 0):
						if (board[i+1][j-1] == 10):
					 		board[i][j]+= 1

					if (i > 0):
						if (board[i-1][j] == 10):
							board[i][j]+= 1

					if (i < size - 1):
						if (board[i+1][j] == 10):
							board[i][j]+= 1

					if (i > 0 and j < size -1):
						if(board[i-1][j+1] == 10):
							board[i][j]+= 1

					if (j < size - 1):
						if(board[i][j+1] == 10):
							board[i][j]+= 1

					if (i < size -1 and j < size - 1):
						if (board[i+1][j+1] == 10):
							board[i][j]+= 1

				if(board[i][j] != 10):
					print(board[i][j], end=" ")
				else:
					print("X", end=" ")
			print()



board = Board(8)


