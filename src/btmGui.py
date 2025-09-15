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
		if "ApplicationTheme" in self.user_data:
			self.display_message("Applying theme in application", "notification")
			try:
				self.THEME = self.user_data["ApplicationTheme"]
				self.theme = self.THEME
			except Exception as e:
				self.display_message(f"Impossible to apply theme\n{traceback.format_exc}", "error")
			else:
				self.display_message(f"Theme applied successfully → {self.user_data["ApplicationTheme"]}", "green")
		self.display_message("Updating informations in Lobby", "notification")
		#check for user credentials in user settings
		if "BrowserHeadless" in self.user_data:
			self.checkbox_headless_browser.value = self.user_data["BrowserHeadless"]
		if "BrowserDifferent" in self.user_data:
			self.checkbox_custom_browser.value = self.user_data["BrowserDifferent"]
		if "BrowserExecutable" in self.user_data:
			self.input_custom_browser.value = self.user_data["BrowserExecutable"]
		if "GroqAPIKey" in self.user_data:
			self.input_groq_apikey.value = self.user_data["GroqAPIKey"]
		if "LinkedinUseAI" in self.user_data:
			self.checkbox_use_groq.value = self.user_data["LinkedinUseAI"]
		if "MaxSavedDisplay" in self.user_data:
			self.input_max_saved.value = str(self.user_data["MaxSavedDisplay"])
		if ("KeywordExcluded" in self.user_data) and (type(self.user_data["KeywordExcluded"])==list):
			self.input_keyword_exclude.value = ";".join(self.user_data["KeywordExcluded"])
		if ("LinkedinUserSkillsExclude" in self.user_data) and (type(self.user_data["LinkedinUserSkillsExclude"])==list):
			self.input_user_exclude_skills.value = ";".join(self.user_data["LinkedinUserSkillsExclude"])
		if ("LinkedinUserLocation" in self.user_data) and (type(self.user_data["LinkedinUserLocation"])==list):
			self.input_user_location.value = ";".join(self.user_data["LinkedinUserLocation"])
		if "LinkedinUserSkills" in self.user_data:
			if type(self.user_data["LinkedinUserSkills"]) == list:
				#convert to str
				user_skill_list = ";".join(self.user_data["LinkedinUserSkills"])
			elif type(self.user_data["LinkedinUserSkills"]) == str:
				user_skill_list = self.user_data["LinkedinUserSkills"]
			else:
				self.display_message("Impossible to convert user skills to list", "error")
				return
			self.input_user_skills.value = user_skill_list

		"""
		if ("LinkedinMail" in self.user_data) and ("LinkedinPassword" in self.user_data):
			self.display_message("Personnal linkedin informations detected in user data", "message")
			self.input_linkedin_username.value = self.user_data["LinkedinMail"]
			self.input_linkedin_password.value = self.user_data["LinkedinPassword"]
		else:
			self.display_message("Personnal linkedin informations missing in user data", "error")
		"""
		
		if ("KeywordRequired" in self.user_data):
			#format data for input field
			final_format = ""
			for category in self.user_data["KeywordRequired"]:
				joined = ";".join(category)
				final_format+=f'[{joined}]'
			self.input_keyword_required.value = final_format

		self.display_message("Updating informations done...", "success")

	def update_scrapping_label_function(self):
		#get values from scrapping data
		#number of post displayed on TUI
		#number of post saved in file (total)
		#number of post checked in file (total)
		try:
			if "LinkedinScrapping" in self.scrapping_file_data:
				self.counter_displayed_post = len(self.scrapping_post_displayed)
				self.counter_saved_post = len(list(self.scrapping_file_data["LinkedinScrapping"].keys()))
				self.counter_checked_post = len(self.scrapping_file_data["LinkedinCheckedPost"])
			self.label_counter_displayed.update(f"Displayed Posts\n{self.counter_displayed_post}")
			self.label_counter_saved.update(f"Saved Posts\n{self.counter_saved_post}")
			self.label_counter_checked.update(f"Checked Posts\n{self.counter_checked_post}")
		except:
			self.call_from_thread(self.display_message, f"Impossible to update scrapping labels\n{traceback.format_exc()}", "error")


	#show saved post from linkedin scrapping in the main interface
	def display_scrapping_function(self):

		self.call_from_thread(self.display_message, "Trying to read saved scrapping datas", "notification")
		self.list_mounted_post_size = 0

		while True:
			#display current "display post limitation"
			#self.call_from_thread(self.display_message, f"Current display post limitation : {self.user_data["MaxSavedDisplay"]}")
			self.update_scrapping_label_function()
			#self.call_from_thread(self.display_message, "refresh...", "message")
			try:
				with open("data/linkedin_scrapping.json", "r") as scrapping_file:
					self.scrapping_file_data = json.load(scrapping_file)
			except FileNotFoundError:
				self.call_from_thread(self.display_message, "No scrapping data saved yet...", "error")
				sleep(5)
			except Exception as e:
				self.call_from_thread(self.display_message, "Impossible to read scrapping content...", "error")
				sleep(5)

			else:
				"""
				check first is the display limit has been updated 
					→ update this information on interface first
				then check for differences in scrapping dictionnary
				"""
				try:
					#try to detect if the display limit has changed
					if self.scrapping_post_display_limit_backup != int(self.user_data["MaxSavedDisplay"]):
						#value updated
						self.call_from_thread(self.display_message, "Max display value updated...")
						
						#detect if post must be removed or loaded?
						#MODIFICATIONS TO MAKE WHEN LIMIT IS UPDATED
						#mount or remove the post on the interface
						#remove from the display list
						#/!\ CHECK IF THE POST IS ALREADY IN THE LIST to avoid mistakes
						if int(self.user_data["MaxSavedDisplay"]) > self.scrapping_post_display_limit_backup:
							#create the list of index between the two numbers
							self.call_from_thread(self.display_message, "add new items", "message")
							index_list = list(range(self.scrapping_post_display_limit_backup, int(self.user_data["MaxSavedDisplay"])))
							for index in index_list:
								#check if index is in list
								try:
									post_to_mount = self.scrapping_post_container[index]
									self.call_from_thread(self.display_message, f"post detected : {index}")
								except Exception as e:
									#self.call_from_thread(self.display_message, f"Impossible to mount post : {e}", "notification")
									pass
								else:
									#mount the post and add it to the displayed post list
									self.call_from_thread(self.vertical_post_container.mount, post_to_mount)
									#update other lists
									if post_to_mount not in self.scrapping_post_displayed:
										self.scrapping_post_displayed.append(post_to_mount)

						if int(self.user_data["MaxSavedDisplay"]) < self.scrapping_post_display_limit_backup:
							self.call_from_thread(self.display_message, "remove items", "message")
							index_list = list(range(int(self.user_data["MaxSavedDisplay"]), self.scrapping_post_display_limit_backup+1))
							for index in index_list:
								try:
									post_to_remove = self.scrapping_post_container[index]
									self.call_from_thread(self.display_message, f"Post detected")
								except Exception as e:
									self.call_from_thread(self.display_message, f"Impossible to remove post : {e}", "notification")
								else:
									#try to remove the post from the interface
									try:
										self.call_from_thread(post_to_remove.remove)
										self.call_from_thread(self.display_message, "Post removed from TUI", "success")
									except Exception as e:
										self.call_from_thread(self.display_message, f"Failed to remove post : {e}", "error")
									else:
										#remove post from lists
										try:
											self.scrapping_post_displayed.remove(post_to_remove)
										except:
											pass

						self.call_from_thread(self.display_message, index_list, "message")
						self.scrapping_post_display_limit_backup = copy.copy(int(self.user_data["MaxSavedDisplay"]))

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
								
								if self.scrapping_post_container.index(post_tui) > int(self.user_data["MaxSavedDisplay"])-1:	
									pass
								else:
									self.call_from_thread(self.vertical_post_container.mount,post_tui)
									self.scrapping_post_displayed.append(post_tui)

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

										#check for the limitation before mounting the post
										if self.scrapping_post_container.index(post_tui) <= self.user_data["MaxSavedDisplay"]-1:
											self.scrapping_post_displayed.append(post_tui)
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
										self.scrapping_post_container.pop(i)

										self.call_from_thread(post_to_remove.remove)

						self.scrapping_file_data_backup = copy.copy(self.scrapping_file_data)
				except Exception as e:
					self.call_from_thread(self.display_message, f"Error happened\n{traceback.format_exc()}", "error")

			#self.call_from_thread(self.display_message, " ", "message", False)
			sleep(1)
