#!/usr/bin/env python
import gi
import random
import sys
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio
from enum import Enum

css = 'grid { border: 2px solid@borders;}#grid-button{ border-radius: 0px; border-width: 2px; border: 1px solid@borders; padding: 0; font-size: 25px;}#size_label{font-size: 15px;}'.encode()
css_provider = Gtk.CssProvider()
css_provider.load_from_data(css)
context = Gtk.StyleContext()
screen = Gdk.Screen.get_default()
context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
global_size = 8


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
				string = "✸"
		return string

# DONE: Win style
# DONE: Ask user for board size
# DONE: HeaderBar
# DONE: Remove prints
# DONE: Start over
# DONE: Bomb exploded proper icon
# DONE: Flag functionality ⚑
# DONE: Built-in CSS

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
		Gtk.Window.__init__(self, resizable=False)

		self.set_border_width(10)
		self.grid = Gtk.Grid(column_spacing=0, row_spacing=0)

		hb = Gtk.HeaderBar()
		hb.set_show_close_button(True)
		hb.props.title = "Minesweeper"
		self.set_titlebar(hb)

		hb_button = Gtk.Button()
		icon = Gio.ThemedIcon(name="view-refresh-symbolic")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		hb_button.connect("clicked", self.startOver)
		hb_button.add(image)
		hb.pack_start(hb_button)

		self.add(self.grid)

		self.board = board
		self.size = size

		#print()
		for i in range(self.size):
			for j in range(self.size):
				eventbox = Gtk.EventBox()
				eventbox.connect("button-press-event", self.on_button_press_event, i, j)

				button = Gtk.ToggleButton(label=board.board[i][j])
				button.connect("clicked", self.on_clicked, i, j)
				button.set_size_request(55,55);

				eventbox.add(button)
				self.grid.attach(eventbox, i, j, 1, 1)
				button.set_name("grid-button")
			#print()


	def on_clicked(self, button, i, j):
		button.set_active(True)
		#print("Click", i, j, "- Board", self.board.board[i][j].value)
		self.click(i,j)

	def on_button_press_event(self, widget, event, i, j):
		button = widget.get_child()
		if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
			if(button.get_label() == "" and button.get_active() == False):
				button.set_label("⚑")
			elif(button.get_label() == "⚑"):
				button.set_label("")

	def update_single_button(self, i, j):
		button = self.grid.get_child_at(i, j).get_child()
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
		self.board.still_hidden = -1
		for i in range(self.size):
			for j in range(self.size):
				self.board.board[i][j].show()
				self.update_single_button(i,j)
				if(self.board.board[i][j].type == TileType.MINE):
					self.grid.get_child_at(i, j).get_child().get_style_context().add_class(Gtk.STYLE_CLASS_DESTRUCTIVE_ACTION)
		dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="Game over")
		dialog.format_secondary_text("Mine exploded")
		dialog.run()
		dialog.destroy()

	def win(self):
		for i in range(self.size):
			for j in range(self.size):
				self.board.board[i][j].show()
				self.update_single_button(i,j)
				if(self.board.board[i][j].type == TileType.MINE):
					self.grid.get_child_at(i, j).get_child().set_label("⚑")
					self.grid.get_child_at(i, j).get_child().get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
		dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="You win!")
		dialog.format_secondary_text("Congratulations")
		dialog.run()
		dialog.destroy()

	def startOver(self, button):
		args = [sys.argv[0], str(self.size)]
		os.execl(sys.executable, os.path.abspath(__file__), *args)
	def showZeros(self, i, j):
		#print("SHOWZEROS: ", i, "", j)
		if(not(i < 0 or i > self.size - 1 or j < 0 or j > self.size - 1)):
			# Don't check tiles out of the board!
			# Show the tile if it is next to a 0 and it is hidden
			if (self.board.board[i][j].hidden):
				self.board.board[i][j].show()
				self.board.still_hidden -= 1
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

class SizeChooserDialog(Gtk.Dialog):
	def __init__(self):
		Gtk.Window.__init__(self, title="New game")
		self.set_border_width(10)
		self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
		self.set_size_request(400,250);

		box = self.get_content_area()
		box.set_spacing(6)

		label = Gtk.Label(label = "Choose the size of the board:")
		box.add(label)
		label.set_name("size_label")
		label.set_vexpand(True)

		self.spin = Gtk.SpinButton()
		self.spin.set_adjustment(Gtk.Adjustment(upper=16, lower=4, step_increment=1))
		self.spin.set_value(8)
		self.spin.connect("value-changed", self.on_value_changed)
		self.spin.set_vexpand(False)
		box.add(self.spin)

		self.label2 = Gtk.Label()
		box.add(self.label2)
		self.label2.set_name("size_label")
		self.label2.set_vexpand(True)
		self.label2.set_markup("Your board will have <b>" + str(pow(self.spin.get_value_as_int(), 2)) + "</b> tiles")

		self.show_all()

		self.connect("response", self.close)

	def on_value_changed(self, spin):
		global global_size
		global_size = self.spin.get_value_as_int()
		self.label2.set_markup("Your board will have <b>" + str(pow(self.spin.get_value_as_int(), 2)) + "</b> tiles")

	def close(self, button, response_id):
		self.destroy()

if (len(sys.argv) < 2):
	size_chooser = SizeChooserDialog()
	size_chooser.run()

else:
	try:
		global_size = int(sys.argv[1])
	except:
		global_size = int(sys.argv[2])


board = Board(global_size)
window = MainWindow(global_size, board)
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
