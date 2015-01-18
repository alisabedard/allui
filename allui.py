#!/usr/bin/env python3

# This is AllUI, an effort to rewrite gtkshell 
# in a portable form, python3/tkinter
# Copyright 2015, Jeffrey E. Bedard <jefbed@gmail.com>

from tkinter import *
from tkinter.ttk import *
import subprocess
import argparse

class GridManager():
	def __init__(self, max=3):
		self.x=0
		self.y=0
		self.__max=max
	def set_max(self, max):
		self.__max=max
	def new_row(self):
		self.y=0
		self.x+=1
	def add(self, target):
		target.grid(row=self.x, column=self.y, sticky=N+S+E+W, 
				padx=2, pady=2)
		self.y+=1
		if(self.y >= self.__max):
			self.new_row()

_grid = GridManager()


class CommandButton(Button):
	def __init__(self, master, text, command=None, command_string=None):
		if(command==None):
			command=self.__run_command
		if(command_string==None):
			command_string=text
		self.__command=command_string
		split_text=text.split('#', maxsplit=1)
		text=split_text[len(split_text)-1].title()
		if(text == "Quit"):
			command=quit
		super().__init__(master=master, text=text, command=command)
		_grid.add(self)
	def __run_command(self):
		print("EXECUTING: " + self.__command)
		subprocess.call(self.__command + "&", shell=True)

class ButtonAction(argparse.Action):
	def __init__(self, parent, option_strings, dest, nargs=None, **kwargs):
		self.__parent=parent
		super().__init__(option_strings, dest, **kwargs)
	def __call__(self, parser, namespace, values, option_string):
		CommandButton(self.__parent, values)

class LabelAction(argparse.Action):
	def __init__(self, parent, option_strings, dest, nargs=None, **kwargs):
		self._parent=parent
		super().__init__(option_strings, dest, **kwargs)
	def __call__(self, parser, namespace, values, option_string):
		label=Label(self._parent, text=values)
		_grid.add(label)

class AllUI(Frame):
	def __init__(self, master=None, title="AllUI"):
		super().__init__(master)
		master.title(title)
		self.parse_args()
		self.grid(sticky=N+S+E+W)
	def parse_args(self):
		parser=argparse.ArgumentParser(description="Generate a GUI")
		parser.add_argument("-l", nargs=1, action=LabelAction, parent=self,
				metavar="LABEL")
		parser.add_argument("-b", nargs=1, action=ButtonAction, parent=self,
				metavar="BUTTON")
		parser.add_argument("BUTTON", nargs='*', action=ButtonAction, parent=self,
				metavar="BUTTON")
		args=parser.parse_args()


def main():
	root=Tk()
	win = AllUI(root)
	root.mainloop()

if __name__ == "__main__":
    main()

