import gi
import random

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from enum import Enum

# Game
class TileType(Enum):
	FREE = 0
	MINE = 1

class Tile:
    def __init__(self, type):
        self.type = type #MINE or FREE
        self.hidden = False
        self.value = 0

    def addMine(self):
        self.value += 1

    def show(self):
        self.hidden = False # TODO: Set to true

    def __str__(self):
        string = ""
        if(self.hidden):
            string = ""
        else:
            if(self.type == TileType.FREE):
                string = str(self.value)
            else:
                string = "X"

        return string

# TODO: Reveal adjacent '0' tiles and first numbered tiles
# TODO: Lose the game if X is clicked

class Board:
	def __init__(self, size):
		self.size = size;
		self.board = [[Tile(TileType.FREE) for i in range(size)] for j in range(size)]
		for i in range(size):
			for j in range(size):
				x = random.uniform(0,1)
				if (x >= 10/64):
					self.board[i][j] = Tile(TileType.FREE) # no mine
					print("0", end=" ")
				else:
					self.board[i][j] = Tile(TileType.MINE) # mine
					print("X", end=" ")

			print()
		print()
		for i in range(size):
			for j in range(size):
				if (self.board[i][j].type == TileType.FREE):
					if (i > 0 and j > 0):
						if (self.board[i-1][j-1].type == TileType.MINE):
							self.board[i][j].addMine()
					if (j > 0):
						if (self.board[i][j-1].type == TileType.MINE):
							self.board[i][j].addMine()

					if (i < size-1 and j > 0):
						if (self.board[i+1][j-1].type == TileType.MINE):
					 		self.board[i][j].addMine()

					if (i > 0):
						if (self.board[i-1][j].type == TileType.MINE):
							self.board[i][j].addMine()

					if (i < size - 1):
						if (self.board[i+1][j].type == TileType.MINE):
							self.board[i][j].addMine()

					if (i > 0 and j < size -1):
						if(self.board[i-1][j+1].type == TileType.MINE):
							self.board[i][j].addMine()

					if (j < size - 1):
						if(self.board[i][j+1].type == TileType.MINE):
							self.board[i][j].addMine()

					if (i < size -1 and j < size - 1):
						if (self.board[i+1][j+1].type == TileType.MINE):
							self.board[i][j].addMine()

				if(self.board[i][j].type != TileType.MINE):
					print(self.board[i][j], end=" ")
				else:
					print("X", end=" ")
			print()

class MainWindow(Gtk.Window):
	def __init__(self, size, board):
		Gtk.Window.__init__(self, title="Minesweeper")
		self.grid = Gtk.Grid()
		self.add(self.grid)

		for i in range(size):
			for j in range(size):
				button = Gtk.Button(label=board.board[i][j])
				self.grid.attach(button, i, j, 1, 1)
				button.connect("clicked", self.on_clicked, i, j)

	def on_clicked(self, button, i, j):
		print("Click", i, j)
		board.board[i][j].show()
		self.update_single_button(i, j)

	def update_single_button(self, i, j):
			button = self.grid.get_child_at(i, j)
			button.set_label(str(board.board[i][j]))
board = Board(8)

window = MainWindow(8, board)
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
