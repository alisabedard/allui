#!/usr/bin/env python3

# This is AllUI, an effort to rewrite gtkshell 
# in a portable form, python3/tkinter
# Copyright 2015, Jeffrey E. Bedard <jefbed@gmail.com>

from tkinter import *
from tkinter.ttk import *
import subprocess
import argparse

class CommandButton(Button):
	def __init__(self, text, command=None, commandString="echo"):
		self.__command=commandString
		if(command==None):
			command=self.__runCommand
		super().__init__(text=text, command=command)
		self.grid()
	def __runCommand(self):
		print("EXECUTING: " + self.__command)
		subprocess.call(self.__command + "&", shell=True)
		

class AllUI(Frame):
	def __init__(self, master=None, title="AllUI", args=None):
		super().__init__(master)
		master.title(title)
		self.parseArgs
	def parseArgs(self, args):
		pass
	def setupButtons(self):
		CommandButton("ls", commandString="ls")
		CommandButton("Quit", quit)

def main():
	win = AllUI(Tk())
	win.setupButtons()
	win.mainloop()

if __name__ == "__main__":
    main()

