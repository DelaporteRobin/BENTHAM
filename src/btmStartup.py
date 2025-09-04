# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import traceback
import threading

import colorama
import pyfiglet

from datetime import datetime
from termcolor import *

from datetime import datetime
from rich.console import Console
from rich.theme import Theme
from rich.traceback import install

starting_path = os.getcwd()
real_path = os.path.dirname(os.path.abspath(__file__))
project_general_path = os.path.dirname(real_path)
project_data_path = os.path.join(project_general_path, "data")

os.chdir(project_general_path)
os.system("title Bentham Startup - Quazar")
print(f'Program path : {real_path}\nProject data path : {project_data_path}')
#add the program to sys path
if project_general_path not in sys.path:
	#sys.path.insert(0, src_path)
	sys.path.insert(0, project_general_path)
	print("Path variables added to sys path")
#import the module
#import themes
try:
	from src.btmLinkedin import BenthamLINKEDIN
	from src.btmUser import BenthamUSER
	from styles.theme_file import *
except Exception:
	print(colored(f"Failed to import modules\n{traceback.format_exc()}", "red"))
	os.system("pause")
	exit()
else:
	print(colored("All required modules imported", "green"))



class BtmStartupApplication(BenthamLINKEDIN, BenthamUSER):

	def __init__(self):
		theme_name = "wine"
		#elite,bloody,blocky,ansi_shadow
		self.pyfiglet_font = "bloody"
		#try to import the theme from file
		for theme in THEME_REGISTRY:
			#self.register_theme(theme)
			if theme.name == theme_name:
				self.THEME = theme
		#create the console
		self.console = Console()
		#load user data
		self.user_data = {}
		#load scrapping data
		self.linkedin_scrapping_table = {}
		self.linkedin_post_checked = []
		self.scrapping_data = {}
		#call loading functions
		self.load_scrapping_data_function()
		self.load_user_data_function()

		#self.console.print("[%s]BENTHAM STARTUP MODULE LAUNCHED"%self.THEME.primary)
		self.display_message("Bentham startup task launched", "notification")
		self.console.print(f'[{self.THEME.primary}]{pyfiglet.figlet_format("BENTHAM STARTUP",font=self.pyfiglet_font)}[/{self.THEME.primary}]')

		try:
			self.stop_thread_linkedin=True
			self.thread_scrapping = threading.Thread(target=self.thread_linkedin_scrapper,args=())
			self.thread_scrapping.start()
			self.display_message("Thread started", "success")
			self.thread_scrapping.join()
			#self.thread_scrapping.join()
			os.system("pause")
		except Exception as e:
			self.display_message("Impossible to launch thread", "error")
			self.display_message(traceback.format_exc(), "error")


	def display_message(self,message=" ", severity = "message", show_time = True):
		if severity == "warning":
			color = self.THEME.warning
		elif severity == "success":
			color = self.THEME.success
		elif severity == "error":
			color = self.THEME.error
		elif severity == "notification":
			color = self.THEME.accent
		else:
			color = "white"

		if show_time == True:
			msg_format = f"[{str(datetime.now)}] [{color}]{severity.upper()}[/{color}] → {str(message)}" 
			log_format = f'[{str(datetime.now())}] {severity.upper()} → {str(message)}\n'
		else:
			msg_format = f"{str(message)}"
			log_format = f'		{str(message)}\n'
		#self.console.print(f'[{}]{str(message)}')
		self.console.print(msg_format)
		#save lines in file
		with open("data/btmLog.log", "a", encoding="utf-8") as log_file:
			log_file.write(log_format)

	#when a function is not callable just recreate it xD
	def call_from_thread(self, function_name, *args, **kwargs):
		self.display_message(*args, **kwargs)

	



#launch the class
try:
	btmstartupclass = BtmStartupApplication()
except Exception:
	print(colored(traceback.format_exc(), "red"))
	os.system("pause")

	
