# -*- coding: utf-8 -*-

from termcolor import *
from rich.console import Console
from rich import print as rprint
from time import sleep
from datetime import datetime 

import traceback
import json
import re 
import argparse
import os 
import colorama
import sys
import subprocess

colorama.init()





class BenthamUSER:
	def save_user_data_function(self):
		self.display_message("Trying to save user data", "notification")
		try:
			with open("data/userData.json", "w") as save_file:
				json.dump(self.user_data, save_file, indent=4)
		except Exception as e:
			self.display_message("Impossible to save user data", "error")
			self.display_message(traceback.format_exc(), "error")
		else:
			self.display_message("User data updated...", "success")

	def load_user_data_function(self):
		self.display_message("Trying to load user data", "notification")
		try:
			with open("data/userData.json", "r") as user_data:
				self.user_data = json.load(user_data)
		except Exception as e:
			self.display_message("Impossible to load user data", "error")
			self.display_message(traceback.format_exc(), "error")
		else:
			self.display_message("User data loaded", "success")

	def save_scrapping_function(self):
		try:
			with open("data/linkedin_scrapping.json", "w") as save_file:
				json.dump(self.linkedin_scrapping_table, save_file, indent=4)
		except Exception as e:
			self.call_from_thread(self.display_message, "Impossible to save scrapping data in file...", "error")
			self.call_from_thread(self.display_message, traceback.format_exc(), "error")
		else:
			self.call_from_thread(self.display_message, "Scrapping data saved successfully", "success")

	def load_scrapping_data_function(self):
		if os.path.isfile("data/linkedin_scrapping.json")==False:
			#self.call_from_thread(self.display_message, "Scrapping data file doesn't exists yet", "warning")
			self.display_message("Scrapping data file doesn't exists yet", "warning")
			return
		else:
			try:
				with open("data/linkedin_scrapping.json", "r") as scrapping_file:
					self.linkedin_scrapping_table = json.load(scrapping_file)
			except Exception as e:
				#self.call_from_thread(self.display_message, "Impossible to load scrapping data from file", "error")
				#self.call_from_thread(self.display_message, traceback.format_exc(), "error", False)
				self.display_message("Impossible to load scrapping data from file", "error")
				self.display_message(traceback.format_exc(), "error", False)
			else:
				#self.call_from_thread(self.display_message, "Scrapping data loaded from file", "success")
				self.display_message("Scrapping data loaded from file", "success")

	#create a window task to trigger the scrapping when the user start computer
	def create_startup_task_function(self):
		self.display_message("Trying to create a startup task")
		script_path = os.path.join(os.getcwd(), "src/btmStartup.py")
		python_path = sys.executable
		command = f'"{python_path}" "{script_path}"'
		taskname = "btmStartupTask"

		try:
			output = subprocess.run([
				"schtasks",
				"/create",
				"/tn",taskname,
				"/tr",command,
				"/sc","onlogon",
				"/rl","HIGHEST",
				"/f"
			])
		except Exception as e:
			self.display_message("Impossible to create the task", "error")
			self.display_message(traceback.format_exc(), "error")
		else:
			if output.returncode == 0:
				self.display_message("Task successfully created", "success")
				self.display_message("Scrapping will startup next time you'll start your computer", "notification")
			else:
				self.display_message("Impossible to create the task", "error")
				self.display_message(str(output, "error"))