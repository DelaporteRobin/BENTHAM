# -*- coding: utf-8 -*-
from textual.app import App, ComposeResult
from textual.widgets import Sparkline, Tree, ProgressBar, Input, RadioSet, MarkdownViewer, RadioButton, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
#from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.screen import Screen, ModalScreen
from textual.await_complete import AwaitComplete
from textual.await_remove import AwaitRemove
from textual.binding import Binding, BindingType
from textual import events
from textual import work
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from textual import on
from textual.events import Mount
from textual.message import Message
from textual.reactive import reactive
from textual.await_complete import AwaitComplete 
from textual.widgets._directory_tree import DirEntry
from textual.widgets._tree import TreeNode
from textual.errors import TextualError
from textual.widgets._list_item import ListItem
from textual.widget import AwaitMount, Widget
from textual.binding import Binding
from textual.geometry import clamp
#import external textual plugins
from textual_pyfiglet import FigletWidget
from textual_slidecontainer import SlideContainer

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
import copy
import colorama

colorama.init()


class Bentham_Modal_PostFormatting(Static):
	def __init__(self, post_id,post_data):
		super().__init__()
		self.post_data = post_data
		self.post_id = post_id

	def compose(self) -> ComposeResult:
		with Collapsible(title = '%s  -  %s'%(self.post_data["postDate"],self.post_data["postAuthor"]), id=f"collapsible_linkedin_post_{self.post_data["postIdentifier"]}"):

			#content of the post
			self.markdown_linkedin_post_content = Markdown(id = "markdown_linkedin_post_content")
			yield self.markdown_linkedin_post_content

			#link of the post
			#yield Label(f"To see the post on linkedin → {self.post_data["postLink"]}")

	def on_mount(self) -> None:
		markdown_content = f'''
{self.post_data["postContent"]}

## To display the post on Linkedin
{self.post_data["postLink"]}
'''
		#self.markdown_linkedin_post_content.update(self.post_data["postContent"])
		self.markdown_linkedin_post_content.update(markdown_content)




class BenthamGUI:
	def update_lobby_informations(self):
		self.display_message("Updating informations in Lobby", "notification")
		#check for user credentials in user settings
		if ("LinkedinMail" in self.user_data) and ("LinkedinPassword" in self.user_data):
			self.display_message("Personnal linkedin informations detected in user data", "message")
			self.input_linkedin_username.value = self.user_data["LinkedinMail"]
			self.input_linkedin_password.value = self.user_data["LinkedinPassword"]
		else:
			self.display_message("Personnal linkedin informations missing in user data", "error")
		
		if ("KeywordRequired" in self.user_data):
			#format data for input field
			final_format = ""
			for category in self.user_data["KeywordRequired"]:
				joined = ";".join(category)
				final_format+=f'[{joined}]'
			self.input_keyword_required.value = final_format

		self.display_message("Updating informations done...", "success")

	#show saved post from linkedin scrapping in the main interface
	def display_scrapping_function(self):

		self.call_from_thread(self.display_message, "Trying to read saved scrapping datas", "notification")
		self.list_mounted_post_size = 0

		while True:
			self.call_from_thread(self.display_message, "refresh...", "message")
			try:
				with open("data/linkedin_scrapping.json", "r") as scrapping_file:
					self.scrapping_file_data = json.load(scrapping_file)
			except FileNotFoundError:
				self.call_from_thread(self.display_message, "No scrapping data saved yet...", "error")
				sleep(10)
			except Exception as e:
				self.call_from_thread(self.display_message, "Impossible to read scrapping content...", "error")
				sleep(10)

			else:
				try:
					"""
					from the content / dictionnary saved in file
						- display all saved posts
						- save the current state of the dictionnary to compare with the new dictionnary
					"""
					#if ("LinkedinScrapping" in self.scrapping_file_data) and (self.scrapping_file_data)
					if self.scrapping_file_data != self.scrapping_file_data_backup:
						self.call_from_thread(self.display_message, "New data detected", "notification")
						
						#get differences in dictionnary
						#if ("LinkedinScrapping" in self.scrapping_file_data) and ("LinkedinScrapping":
						if ("LinkedinScrapping" in self.scrapping_file_data) and ("LinkedinScrapping" not in self.scrapping_file_data_backup):
							self.call_from_thread(self.display_message, "Init scrapping display", "message")
							self.call_from_thread(self.display_message, f"{len(list(self.scrapping_file_data["LinkedinScrapping"].keys()))} post(s) detected")
							#send all post to display
							for post_id, post_data in self.scrapping_file_data["LinkedinScrapping"].items():
								post_tui = Bentham_Modal_PostFormatting(post_id, post_data)
								self.scrapping_post_container.append(post_tui)
								self.call_from_thread(self.vertical_post_container.mount,post_tui)

						if ("LinkedinScrapping" in self.scrapping_file_data) and ("LinkedinScrapping" in self.scrapping_file_data_backup):
							#check for differences
							self.call_from_thread(self.display_message, "Check differences...", "message")

							#EQUAL SIZE
							if len(list(self.scrapping_file_data["LinkedinScrapping"].keys())) == len(list(self.scrapping_file_data_backup["LinkedinScrapping"].keys())):
								self.call_from_thread(self.display_message, "No difference detected", "message")

							#NEW POST ADDED
							elif len(list(self.scrapping_file_data["LinkedinScrapping"].keys())) > len(list(self.scrapping_file_data_backup["LinkedinScrapping"].keys())):
								self.call_from_thread(self.display_message, "New posts to display", "message")
								#go through each key of the new dictionnary
								#get keys which are not saved in the backup dictionnary
								#display these posts
								for post_id, post_data in self.scrapping_file_data["LinkedinScrapping"].items():
									if post_id not in self.scrapping_file_data_backup["LinkedinScrapping"]:
										post_tui = Bentham_Modal_PostFormatting(post_id, post_data)
										self.scrapping_post_container.append(post_tui)
										self.call_from_thread(self.vertical_post_container.mount,post_tui)

							#A POST TO REMOVE?
							else:
								self.call_from_thread(self.display_message, "Post to remove", "message")
								#go through each key of the backup dictionnary
								#get the index of all post id not in dictionnary anymore
								#remove the related post layout from the TUI
								list_backup_post = list(self.scrapping_file_data_backup["LinkedinScrapping"].keys())
								for i in range(len(list_backup_post)):
									if list_backup_post[i] not in self.scrapping_file_data["LinkedinScrapping"]:
										self.call_from_thread(self.display_message, f"Post to remove detected : {[i]}") 
										#widget / container to remove
										post_to_remove = self.scrapping_post_container[i]
										self.call_from_thread(post_to_remove.remove)
										self.scrapping_post_container.pop(i)

						self.scrapping_file_data_backup = copy.copy(self.scrapping_file_data)
				except Exception as e:
					self.call_from_thread(self.display_message, f"Error happened\n{traceback.format_exc()}", "error")

			self.call_from_thread(self.display_message, " ", "message", False)
			sleep(5)

		"""
		try:
			self.list_mounted_post_size = 0
			self.call_from_thread(self.display_message, "Starting to read saved linkedin posts...", "notification")
			#GET THE CONTENT OF THE SCRAPPING LOG IF IT EXISTS
			#for i in range(50):
			with open("data/linkedin_scrapping.json", "r") as scrapping_file:
				scrapping_content = json.load(scrapping_file)
			table_post = scrapping_content["LinkedinScrapping"]
			
			if len(list(table_post.keys())) != self.list_mounted_post_size:
				
				
				for post_id, post_data in table_post.items():
					post_tui = Bentham_Modal_PostFormatting(post_id,post_data)

					#mount the formatted post tui in the vertical scroll contained
					self.call_from_thread(self.vertical_post_container.mount,post_tui)
			



			self.call_from_thread(self.display_message, self.vertical_post_container.children)
		except Exception as e:
			self.call_from_thread(self.display_message, "Scrapping reader failed", "error")
			self.call_from_thread(self.display_message, traceback.format_exc(), "error")
		"""