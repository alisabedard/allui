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
		self.row=0
		self.column=0
		self.__max=max
	def set_max(self, max):
		self.__max=max
	def new_row(self):
		self.column=0
		self.row+=1
	def add(self, target, **kwargs):
		target.grid(row=self.row, column=self.column, sticky=N+S+E+W, 
				padx=2, pady=2, **kwargs)
		self.column+=1
		if(self.column >= self.__max):
			self.new_row()

_grid = GridManager()


class CommandButton(Button):
	def __init__(self, master, text, command=None, command_string=None):
		if command is None:
			command=self.__run_command
		if command_string is None:
			command_string=text
		self.__command=command_string
		split_text=text.split('#', maxsplit=1)
		text=split_text[len(split_text)-1].title()
		if(text == "Quit"):
			command=quit
		super().__init__(master=master, text=text, command=command)
	def __run_command(self):
		print("EXECUTING: " + self.__command)
		subprocess.call(self.__command + "&", shell=True)

class CompoundEntry(Frame):
	def __init__(self, parent, prompt):
		super().__init__(master=parent)
		self.__prompt=prompt
		label=Label(self, text=prompt)
		label.grid(row=0, column=0, padx=2)
		text = Entry(self)
		text.grid(row=0, column=2, columnspan=2)
		self.__text=text
		button = CommandButton(self, text="Submit", command=self.__entry_submit)
		button.grid(row=0, column=4, padx=4, pady=2)
	def __entry_submit(self):
		print(self.__prompt + ':' + self.__text.get())

class WidgetAction(argparse.Action):
	def __init__(self, parent, option_strings, dest, nargs=None, **kwargs):
		self._parent=parent
		super().__init__(option_strings, dest, **kwargs)
	def __call__(self, parser, namespace, values, option_string):
		if option_string == '-e':
			widget=CompoundEntry(self._parent, values)
		elif option_string == '-l':
			widget=Label(self._parent, text=values)
		elif option_string == '-r':
			_grid.set_max(int(values))	
			_grid.new_row()
			return
		else:
			widget=CommandButton(self._parent, values)
		_grid.add(widget)

class AllUI(Frame):
	def __init__(self, master=None, title="AllUI"):
		super().__init__(master)
		master.title(title)
		self.parse_args()
		self.grid(sticky=N+S+E+W)
	def parse_args(self):
		parser=argparse.ArgumentParser(description="Generate a GUI")
		parser.add_argument('-l', '--label',nargs=1, action=WidgetAction, parent=self,
				metavar="LABEL")
		button_help="Define a button which executes the specified shell command. "
		button_help+="Put the button label definition after a '#' comment character."
		parser.add_argument('-b', '--button', nargs=1, action=WidgetAction, 
				parent=self, metavar="BUTTON", help=button_help)
		parser.add_argument('-e', action=WidgetAction, parent=self, metavar='NAME')
		parser.add_argument('-r', action=WidgetAction, parent=self, metavar='MAX')
		args=parser.parse_args()


def main():
	root=Tk()
	win = AllUI(root)
	root.mainloop()

if __name__ == "__main__":
    main()

