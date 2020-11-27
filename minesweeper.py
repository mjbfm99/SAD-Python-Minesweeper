import gi
import random
import sys
#sys.tracebacklimit = 0

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from enum import Enum

# Game
class TileType(Enum):
	FREE = 0
	MINE = 1

class Tile:
    def __init__(self, type):
        self.type = type #FREE, MINE
        self.hidden = False # TODO: Set to true
        if type == TileType.MINE:
            self.value = 9
        else:
            self.value = 0

    def addMine(self):
        self.value += 1

    def show(self):
        self.hidden = False

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
					#print("0", end=" ")
				else:
					self.board[i][j] = Tile(TileType.MINE) # mine
					#print("X", end=" ")

			#print()
		#print()
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

				#if(self.board[i][j].type != TileType.MINE):
					#print(self.board[i][j].value, end=" ")
				#else:
					#print("X", end=" ")
			#print()

		for j in range(size):
			for i in range(size):
				print(self.board[i][j], end=" ")
			print()

class MainWindow(Gtk.Window):
	def __init__(self, size, board):
		Gtk.Window.__init__(self, title="Minesweeper", resizable=False)
		self.set_border_width(10)
		self.grid = Gtk.Grid(column_spacing=4, row_spacing=4)
		self.add(self.grid)
		self.board = board
		self.size = size
		#print()
		for i in range(size):
			for j in range(size):
				#print(board.board[i][j], end=" ")
				button = Gtk.Button(label=board.board[i][j])
				#button = Gtk.Button(label=str(i) + " " + str(j))
				button.connect("clicked", self.on_clicked, i, j)
				button.set_size_request(50,50);
				self.grid.attach(button, i, j, 1, 1)
			#print()


	def on_clicked(self, button, i, j):
		print("Click", i, j, "- Board", self.board.board[i][j].value)
		self.click(j,i)

	def update_single_button(self, i, j):
			button = self.grid.get_child_at(i, j).set_label(str(board.board[i][j]))

	def click(self, i, j):
		size = self.size
		if (self.board.board[i][j].type == TileType.FREE and self.board.board[i][j].hidden):
			self.board.board[i][j].show()
			self.update_single_button(i,j)
			if (self.board.board[i][j].value == 0):
				if (i > 0 and j > 0):
					if (self.board.board[i-1][j-1].value == 0 and self.board.board[i-1][j-1].hidden):
						self.click(i-1,j-1)
					else:
						self.board.board[i-1][j-1].show()
						self.update_single_button(i-1,j-1)

				if (j > 0):
					if (self.board.board[i][j-1].value == 0 and self.board.board[i-1][j-1].hidden):
						self.click(i,j-1)
					else:
						self.board.board[i][j-1].show()
						self.update_single_button(i,j-1)

				if (i < size-1 and j > 0):
					if (self.board.board[i+1][j-1].value == 0 and self.board.board[i-1][j-1].hidden):
				 		self.click(i+1,j-1)
					else:
						self.board.board[i+1][j-1].show()
						self.update_single_button(i+1,j-1)

				if (i > 0):
					if (self.board.board[i-1][j].value == 0 and self.board.board[i-1][j-1].hidden):
						self.click(i-1,j)
					else:
						self.board.board[i-1][j].show()
						self.update_single_button(i-1,j)

				if (i < size - 1):
					if (self.board.board[i+1][j].value == 0 and self.board.board[i-1][j-1].hidden):
						self.click(i+1,j)
					else:
						self.board.board[i+1][j].show()
						self.update_single_button(i+1,j)

				if (i > 0 and j < size -1):
					if(self.board.board[i-1][j+1].value == 0 and self.board.board[i-1][j-1].hidden):
						self.click(i-1,j+1)
					else:
						self.board.board[i-1][j+1].show()
						self.update_single_button(i-1,j+1)

				if (j < size - 1):
					if(self.board.board[i][j+1].value == 0 and self.board.board[i-1][j-1].hidden):
						self.click(i,j+1)
					else:
						self.board.board[i][j-1].show()
						self.update_single_button(i,j-1)

				if (i < size -1 and j < size - 1):
					if (self.board.board[i+1][j+1].value == 0 and self.board.board[i-1][j-1].hidden):
						self.click(i+1,j+1)
					else:
						self.board.board[i+1][j+1].show()
						self.update_single_button(i+1,j+1)

board = Board(5)

window = MainWindow(5, board)
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
