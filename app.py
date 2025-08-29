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

from datetime import datetime
from typing import Any

from rich.console import Console
from rich.theme import Theme
from rich.traceback import install

#import external modules
from src.btmLinkedin import BenthamLINKEDIN
from src.btmUser import BenthamUSER
from src.btmGui import BenthamGUI
from src.btmUtility import BenthamUTILITY

import re
import multiprocessing as mp 
import threading
import sys
import os 
import traceback
import copy


class Bentham_Main(App, BenthamLINKEDIN, BenthamUSER, BenthamGUI, BenthamUTILITY):

	CSS_PATH = ["styles/layout.tcss"]
	BINDINGS = [
		Binding("+", "binding_logs", description="Show logs", key_display="+")
	]

	def __init__(self):
		super().__init__()
		#init user program before creating main interface
		self.rich_theme = Theme(
			{
				"general":"dark_violet",
				"info":"yellow",
				"warning":"orange3",
				"error":"red3",
				"success":"chartreuse1",
			}
		)
		self.list_display_mode = [
			("Sorted by relevance",0),
			("Sorted by most recent",1)
		]
		#create the rich console
		self.console = Console(theme=self.rich_theme)
		#user informations here
		self.user_data = {}
		self.linkedin_cookies = {}
		self.linkedin_scrapping_table = {}
		self.linkedin_post_checked = []
		self.scrapping_data = {}
		self.scrapping_file_data = {}
		self.scrapping_file_data_backup = copy.copy(self.scrapping_file_data)
		self.scrapping_post_container = []
		#keyword list for linkedin parsing
		self.list_keyword_required = []
		self.list_keyword_pertinent = []
		
		#thread init variable
		self.stop_thread_linkedin = False
		self.lock_log_file = threading.Lock()

	def compose(self) -> ComposeResult:
		yield Header(show_clock=True)
		"""
		MAIN GUI CREATION
		left column → options for the linkedin scrapper
		right column → linkedin posts
		"""
		with Horizontal(id = "horizontal_main_container"):
			with SlideContainer(id = "slidecontainer_right", slide_direction="right", dock_position="right", fade=True, duration=0.5, start_open=False):
				self.listview_log = ListView(id = "listview_log")
				yield self.listview_log
				self.listview_log.border_title = "Application log"
			with VerticalScroll(id = "vertical_column_left"):
				with Collapsible(title = "Linkedin authentification", id="collapsible_authentification"):
					self.input_linkedin_username = Input(placeholder="Linkedin mail or phone", id="input_linkedin_username")
					self.input_linkedin_password = Input(placeholder = "Linkedin password", password=True, id="input_linkedin_password")

					yield self.input_linkedin_username
					yield self.input_linkedin_password
					yield Button("Get linkedin cookies", id = "button_get_cookies")

				with Collapsible(title = "Linkedin scrapping settings",id = "collapsible_settings"):
					#yield Button("hello world")
					#change the linkedin display mode
					self.select_linkedin_displaymode = Select(self.list_display_mode,id="select_linkedin_displaymode", value=1)
					yield self.select_linkedin_displaymode

					#self.input_min_day_value = Input(placeholder="Minimum day value", id="input_min_day_value",type="integer",value="0")
					self.input_max_day_value = Input(placeholder="Maximum day value", id="input_max_day_value",type="integer",value="10")					
					self.input_max_scrolling = Input(placeholder="Max scrolling iteration value",id="input_max_scrolling", type="integer", value="150")
					self.input_max_already_saved = Input(placeholder='Max "already saved" post reached', id="input_max_already_saved", type="integer", value="500")

					#yield self.input_min_day_value
					yield Label('Max "already saved" post reached', id="label_max_already_saved")
					yield self.input_max_day_value
					yield Label("Max scrolling iteration value", id="label_max_scrolling")
					yield self.input_max_scrolling
					yield Label("Max day value",id="label_max_day_value")
					yield self.input_max_already_saved

					self.checkbox_startup_mode = Checkbox("Start scrapping at startup", value=False, id="checkbox_startup_mode")
					yield self.checkbox_startup_mode

				#keyword that are all required in the post
				self.input_keyword_required = Input(placeholder="All required keywords", id="input_keyword_required")
				self.input_keyword_pertinent = Input(placeholder="All keywords that might concern you",id="input_keyword_pertinent")

				yield self.input_keyword_required
				yield self.input_keyword_pertinent
				with Horizontal(id = "horizontal_column_scrapping"):
					yield Button("START SCRAPPING", id="button_scrapping_start")
					yield Button("STOP SCRAPPING", id="button_scrapping_stop")
				#yield Button("remove children", id="button_remove_children")


			with VerticalScroll(id = "vertical_column_right"):
				yield Label("Linkedin posts")
				
				self.vertical_post_container = VerticalScroll(id = "vertical_post_container")
				yield self.vertical_post_container

		yield Footer()

	#NOTIFICATION FUNCTION
	def display_message(self,message,severity="message",display_time=True):
		msg = str(message)

		if display_time == True:
			format_msg = "%s | %s: %s"%(str(datetime.now()),severity.upper(),msg)
		else:
			format_msg = "	  %s"%(msg)

		#create the label
		label = Label(format_msg)
		#color the label
		if severity == "success":
			color = "success"
		elif severity == "warning":
			color = "warning"
		elif severity == "notification":
			color = "accent"
		elif severity == "error":
			color = "error"
		else:
			color = "foreground"
		label.styles.color = self.theme_variables[color]
		#display also a rich message for suspended app
		self.console.print("%s - [%s]%s[/%s] → %s"%(str(datetime.now()),self.theme_variables[color],severity.upper(),self.theme_variables[color],msg))
		#save the line in a file

		#lock the file
		try:
			self.lock_log_file.acquire()
			#write log line
			with open("data/btmLog.log", "a", encoding="utf-8") as log_file:
				log_file.write("%s\n"%str(format_msg))
			#release the lock
			self.lock_log_file.release()
		except Exception as e:
			pass
			#self.listview_log.append(ListItem(Label(str(traceback.format_exc()))))
		#update the log listview
		#check for the number of items already contained in the list
		#limit is set to 150?

		
		if len(self.listview_log.children)==150:
			self.listview_log.pop(0)
		
		#add the new item to the listview :)
		self.listview_log.append(ListItem(label))
		self.listview_log.scroll_end()

	#BINDINGS FUNCTION
	def action_binding_logs(self) -> None:
		self.query_one("#slidecontainer_right").toggle()

	def on_mount(self) -> None:
		self.display_message("Welcome in Bentham", "notification")
		#load user data
		self.load_user_data_function()
		self.load_scrapping_data_function()
		#update the interface
		self.update_lobby_informations()
		#launch the thread to read scrapping live
		self.thread_display_scrapping = threading.Thread(target=self.display_scrapping_function, args=(), daemon=True)
		self.thread_display_scrapping.start()

	def on_checkbox_changed(self, event:Checkbox.Changed) -> None:
		if event.checkbox.id == "checkbox_startup_mode":
			if self.checkbox_startup_mode.value==True:
				#create the task for the autorun
				self.create_startup_task_function()

	def on_select_changed(self, event:Select.Changed) -> None:
		if event.select.id == "select_linkedin_displaymode":
			#save the value in user settings dictionnary
			self.user_data["LinkedinDisplayMode"] = self.select_linkedin_displaymode.value
			self.save_user_data_function()

	def on_input_submitted(self, event:Input.Submitted) -> None:
		if event.input.id == "input_min_day_value":
			self.user_data["MinDayValue"] = self.input_min_day_value.value
			self.save_user_data_function() 
		if event.input.id == "input_max_day_value":
			self.user_data["MaxDayValue"] = self.input_max_day_value.value
			self.save_user_data_function()
		if (event.input.id == "input_keyword_required") or (event.input.id == "input_keyword_pertinent"):
			#get the content of the input
			#split the content by | 
			table_keyword_required = []
			splited_keyword_required = smatches = re.findall(r'\[([^\]]+)\]', self.input_keyword_required.value)
			for i in range(len(splited_keyword_required)):
				parsed_keyword_list = []
				splited_element = splited_keyword_required[i].split(";")
				for element in splited_element:
					if self.check_letter_function(element)==True:
						parsed_keyword_list.append(element)
				table_keyword_required.append(parsed_keyword_list)
			#splited_keyword_pertinent = matches = re.findall(r'\[([^\]]+)\]', text)
			#final_keyword_required = []
			#final_keyword_pertinent = []
			#check if each element of the list contain letters
			"""
			for i in range(len(splited_keyword_required)):
				if self.check_letter_function(splited_keyword_required[i])==True:
					final_keyword_required.append(splited_keyword_required[i])
			for i in range(len(splited_keyword_pertinent)):
				if self.check_letter_function(splited_keyword_pertinent[i])==True:
					final_keyword_pertinent.append(splited_keyword_pertinent[i])
			self.user_data["KeywordRequired"]=final_keyword_required
			self.user_data["KeywordPertinent"]=final_keyword_pertinent
			"""

			#[hiring;hire;recrute;recrutement][modélisation;modeling;lookdev;lighting;texturing;surfacing;rendering]
			self.user_data["KeywordRequired"]=table_keyword_required
			#save list in user data
			self.save_user_data_function()
		
	def on_button_pressed(self, event:Button.Pressed) -> None:
		if event.button.id == "button_get_cookies":
			with self.suspend():
				value = self.get_linkedin_cookies_function()
				if value == True:
					#update password and username in user settings
					self.user_data["LinkedinMail"] = self.input_linkedin_username.value
					self.user_data["LinkedinPassword"] = self.input_linkedin_password.value
					self.save_user_data_function()
				os.system("pause")

		if event.button.id == "button_scrapping_start":
			#start a threading event
			
			try:
				self.stop_thread_linkedin=True
				self.thread_scrapping = threading.Thread(target=self.thread_linkedin_scrapper,args=(), daemon=True)
				self.thread_scrapping.start()
				self.display_message("Thread started", "success")
			except Exception as e:
				self.display_message("Impossible to launch thread", "error")
				self.display_message(traceback.format_exc(), "error")

		if event.button.id == "button_scrapping_stop":
			#change the value of the thread theme_variables
			self.stop_thread_linkedin = False
			#try to terminate the driver




		




if __name__ == "__main__":
	Bentham_Main().run()

