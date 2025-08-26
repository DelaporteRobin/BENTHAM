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