import gi
import random
import sys
sys.tracebacklimit = 3

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio
from enum import Enum

css = 'grid {border: 2px solid@borders;} #grid-button{ border-radius: 0px; border-width: 2px; border: 1px solid@borders;'
css_provider = Gtk.CssProvider()
css_provider.load_from_file(Gio.File.new_for_path('styles.css'))
context = Gtk.StyleContext()
screen = Gdk.Screen.get_default()
context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

# Game
class TileType(Enum):
	FREE = 0
	MINE = 1

class Tile:
	def __init__(self, type):
		self.type = type #FREE, MINE
		self.hidden = True
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
			if(self.type == TileType.FREE and self.value != 0):
				string = str(self.value)
			elif(self.type == TileType.MINE):
				string = "💣"
		return string

# TODO: Win style
# TODO: Ask user for board size
# TODO: HeaderBar
# TODO: Remove prints
# TODO: Start over
# TODO: Bomb exploded proper icon
# TODO: Flag functionality

class Board:
	def __init__(self, size):
		self.size = size;
		self.board = [[Tile(TileType.FREE) for i in range(size)] for j in range(size)]
		self.still_hidden = 0
		for i in range(size):
			for j in range(size):
				x = random.uniform(0,1)
				if (x >= 10/64):
					self.board[i][j] = Tile(TileType.FREE) # no mine
					self.still_hidden += 1
					#print(self.still_hidden, end=" ")
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
	def print(self):
		for j in range(self.size):
			for i in range(self.size):
				print(self.board[i][j].value, end=" ")
			print()


class MainWindow(Gtk.Window):
	def __init__(self, size, board):
		Gtk.Window.__init__(self, title="Minesweeper", resizable=False)
		self.set_border_width(10)
		self.grid = Gtk.Grid(column_spacing=0, row_spacing=0)
		self.add(self.grid)
		self.board = board
		self.size = size
		#print()
		for i in range(size):
			for j in range(size):
				#print(board.board[i][j], end=" ")
				button = Gtk.ToggleButton(label=board.board[i][j])
				#button = Gtk.Button(label=str(i) + " " + str(j))
				button.connect("clicked", self.on_clicked, i, j)
				button.set_size_request(55,55);
				self.grid.attach(button, i, j, 1, 1)
				button.set_name("grid-button")
			#print()


	def on_clicked(self, button, i, j):
		button.set_active(True)
		#print("Click", i, j, "- Board", self.board.board[i][j].value)
		self.click(i,j)

	def update_single_button(self, i, j):
		button = self.grid.get_child_at(i, j)
		button.set_active(True)
		button.set_label(str(board.board[i][j]))

	def click(self, i, j):
		size = self.size
		if (self.board.board[i][j].type == TileType.FREE and self.board.board[i][j].hidden):
			if (self.board.board[i][j].value == 0):
				self.showZeros(i, j)
			else:
				board.still_hidden -= 1
				self.board.board[i][j].show()
				self.update_single_button(i,j)
			if(board.still_hidden == 0):
				self.win()
		elif (self.board.board[i][j].type == TileType.MINE and self.board.board[i][j].hidden):
			#Lose the game
			self.lose()
		#print(board.still_hidden)

	def lose(self):
		# Uncover all
		board.still_hidden = -1
		for i in range(self.size):
			for j in range(self.size):
				self.board.board[i][j].show()
				self.update_single_button(i,j)
				if(self.board.board[i][j].type == TileType.MINE):
					self.grid.get_child_at(i, j).get_style_context().add_class(Gtk.STYLE_CLASS_DESTRUCTIVE_ACTION)
		dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="Game over")
		dialog.format_secondary_text("Mine exploded")
		dialog.run()
		dialog.destroy()

	def win(self):
		dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="You win!")
		dialog.format_secondary_text("Congratulations")
		dialog.run()
		dialog.destroy()
	def showZeros(self, i, j):
		#print("SHOWZEROS: ", i, "", j)
		if(not(i < 0 or i > self.size - 1 or j < 0 or j > self.size - 1)):
			# Don't check tiles out of the board!
			# Show the tile if it is next to a 0 and it is hidden
			if (self.board.board[i][j].hidden):
				self.board.board[i][j].show()
				board.still_hidden -= 1
				self.update_single_button(i,j)
				# And then, if it is another 0
				if(self.board.board[i][j].value == 0):
					self.showZeros(i + 1, j)
					self.showZeros(i - 1, j)
					self.showZeros(i, j + 1)
					self.showZeros(i, j - 1)
					self.showZeros(i + 1, j + 1)
					self.showZeros(i + 1, j - 1)
					self.showZeros(i - 1, j + 1)
					self.showZeros(i - 1, j - 1)


board = Board(8)
#board.print()
window = MainWindow(8, board)
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
