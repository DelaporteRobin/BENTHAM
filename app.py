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
#TEXTUAL PYFIGLET
from textual_pyfiglet.figletwidget import FigletWidget

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

#import color themes
from styles.theme_file import *

import re
import multiprocessing as mp 
import threading
import sys
import os 
import traceback
import copy


#modal screen to ask for cookies creation
class Modal_Bentham_AskCookies(ModalScreen, BenthamLINKEDIN, BenthamUTILITY):
	def __init__(self):
		self.app.display_message("hello world","success")
		self.login_done = False
		super().__init__()

	def compose(self) -> ComposeResult:
		with VerticalScroll(id = "modal_askcookies_vertical"):
			self.modal_figlet_cookies = FigletWidget(
				"SAVE COOKIES",
				font="modular",
				justify="center",
				animation_type="gradient",
				colors=["$primary", "$error", "$warning", "$panel"],
				animate=True,
				fps=25,
				gradient_quality=60,
				id = "modal_figlet_cookies"
			)
			yield self.modal_figlet_cookies
			yield Label("Connect to your Linkedin Account and validate to save login cookies")

			with Horizontal(id="modal_askcookies_horizontal"):
				yield Button("Validate", id="modal_askcookies_button_validate")
				yield Button("Cancel",id="modal_askcookies_button_cancel")

	
	def on_mount(self):
		#self.get_linkedin_cookies_function()
		try:
			self.thread_get_cookies = threading.Thread(target=self.get_linkedin_cookies_function)
			self.thread_get_cookies.start()
			self.app.display_message("Launching thread", "success")
		except Exception as e:
			self.app.display_message(f"Impossible to launch driver\n{traceback.format_exc()}", "error")

	def on_button_pressed(self, event:Button.Pressed) -> None:
		if event.button.id == "modal_askcookies_button_cancel":
			self.login_done = None
			
		if event.button.id == "modal_askcookies_button_validate":
			self.login_done=True
			sleep(1)

		self.app.pop_screen()
		self.app.uninstall_screen("Modal_Bentham_AskCookies")


	def on_resize(self) -> None:
		"""Handle the resize event."""
		self.modal_figlet_cookies.refresh_size()


class Bentham_Main(App, BenthamLINKEDIN, BenthamUSER, BenthamGUI, BenthamUTILITY):

	CSS_PATH = ["styles/layout.tcss"]
	"""
	BINDINGS = [
		Binding("+", "binding_logs", description="Show logs", key_display="+")
	]
	"""

	def __init__(self):
		super().__init__()
		#load color themes
		self.THEME_REGISTRY = THEME_REGISTRY
		self.THEME_DICTIONNARY = None
		self.THEME= "alert"
		for theme in self.THEME_REGISTRY:
			self.register_theme(theme)
			if theme.name == self.THEME:
				self.THEME_DICTIONNARY = theme 
		self.theme = self.THEME
		

		#init user program before creating main interface
		"""
		self.rich_theme = Theme(
			{

				"general":"dark_violet",
				"info":"yellow",
				"warning":"orange3",
				"error":"red3",
				"success":"chartreuse1",
			}
		)
		#create the rich console
		self.console = Console(theme=self.rich_theme)
		"""
		self.intro_markdown = '''
## Welcome on Bentham
Created by **Quazar**\n
Your personal LinkedIn feed reader.
You can ask it to search your feed by keywords, \nor use AI to determine the relevance of a post to you.\n
Repo available on [Github](https://github.com/DelaporteRobin/BENTHAM)

> "Everything should be made as simple as possible, but not simpler"\n**Albert Einstein**

If you want some help or learn more about how to use the App,
you can go read the documentation on Notion

> [!NOTE]
> You can access the documentation [Here](https://www.notion.so/BENTHAM-DOCUMENTATION-265f29fde0e380159f4ee8d27ddfdfa7?source=copy_link)


 
'''
		self.list_display_mode = [
			("Sorted by relevance",0),
			("Sorted by most recent",1)
		]
		self.webbrowser_list = [
			("Brave",1),
			("Chrome",2),
			]
		
		#user informations here
		self.user_data = {
			"MinDayValue":0,
			"MaxDayValue":10,
			"MaxSavedDisplay":5,
		}
		self.linkedin_cookies = {}
		self.linkedin_scrapping_table = {}
		self.linkedin_post_checked = []
		self.scrapping_data = {}
		self.scrapping_file_data = {}
		self.scrapping_file_data_backup = copy.copy(self.scrapping_file_data)

		self.scrapping_post_container = []
		self.scrapping_post_displayed = []
		self.scrapping_post_display_limit_backup = 0
		#keyword list for linkedin parsing
		self.list_keyword_required = []
		self.list_keyword_pertinent = []

		#init scrapping label values
		self.counter_displayed_post = "XXX"
		self.counter_saved_post = "XXX"
		self.counter_checked_post = "XXX"
		
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
			"""
			with SlideContainer(id = "slidecontainer_right", slide_direction="right", dock_position="right", fade=True, duration=0.5, start_open=False):
				self.listview_log = ListView(id = "listview_log")
				yield self.listview_log
				self.listview_log.border_title = "Application log"
			"""
			
			
			with VerticalScroll(id = "vertical_column_left"):
				with Vertical(id = "vertical_title_container"):
					"""
					INTERESTING FRONTS
					modular
					ansi_shadow
					ansi
					the_edge
					"""
					self.figlet_app_title = FigletWidget(
						"_-BENTHAM-_",
						font="modular",
						justify="center",
						animation_type="gradient",
						colors=["$primary", "$error", "$warning", "$panel"],
						animate=True,
						fps=25,
						gradient_quality=60,
						id = "figlet_app_title"
						)
					yield self.figlet_app_title
					self.markdown_app_intro = Markdown(self.intro_markdown, id="markdown_app_intro")
					yield self.markdown_app_intro
				with Collapsible(title = "Global settings", id="collapsible_authentification"):

					with Horizontal(id = "horizontal_browser_settings"):
						self.checkbox_custom_browser = Checkbox("Use a custom browser", id="checkbox_custom_browser", value=False)
						self.checkbox_headless_browser = Checkbox("Headless browser", id="checkbox_headless_browser", value=False)
						self.checkbox_startup_mode = Checkbox("Startup mode", id="checkbox_startup_mode", value=False)

						yield self.checkbox_headless_browser
						yield self.checkbox_custom_browser
						yield self.checkbox_startup_mode

					self.input_custom_browser = Input(placeholder="Custom browser executable path", id="input_custom_browser", disabled=True)
					yield self.input_custom_browser

					yield Rule(line_style="heavy")

					"""
					yield Label("Linkedin login informations")
					self.input_linkedin_username = Input(placeholder="Linkedin mail or phone", id="input_linkedin_username")
					self.input_linkedin_password = Input(placeholder = "Linkedin password", password=True, id="input_linkedin_password")
					yield self.input_linkedin_username
					yield self.input_linkedin_password
					"""
					yield Button("Get linkedin cookies", id = "button_get_cookies")

					yield Rule(line_style="heavy")

					#groq settings
					yield Label("Groq AI Informations")
					self.input_groq_apikey = Input(placeholder = "Groq Api Key", id="input_groq_apikey")
					yield self.input_groq_apikey

				with Collapsible(title = "Linkedin scrapping settings",id = "collapsible_settings"):
					#yield Button("hello world")
					#change the linkedin display mode
					self.select_linkedin_displaymode = Select(self.list_display_mode,id="select_linkedin_displaymode", value=1)
					yield self.select_linkedin_displaymode

					yield Rule(line_style="heavy")

					self.input_min_day_value = Input(placeholder="Minimum day value", id="input_min_day_value",type="integer",value="0")
					self.input_max_day_value = Input(placeholder="Maximum day value", id="input_max_day_value",type="integer",value="10")					
					self.input_max_scrolling = Input(placeholder="Max scrolling iteration value",id="input_max_scrolling", type="integer", value="150")
					self.input_max_already_saved = Input(placeholder='Max "already saved" post reached', id="input_max_already_saved", type="integer", value="500")

					
					yield Label('Max "already saved" post reached', id="label_max_already_saved")
					yield self.input_max_already_saved
					yield Label("Max scrolling iteration value", id="label_max_scrolling")
					yield self.input_max_scrolling
					yield Label("Min day value", id="label_min_day_value")
					yield self.input_min_day_value
					yield Label("Max day value",id="label_max_day_value")
					yield self.input_max_day_value



				#keyword that are all required in the post
				self.input_keyword_required = Input(placeholder="All required keywords", id="input_keyword_required")
				self.input_keyword_exclude = Input(placeholder = "All excluded keywords", id="input_keyword_exclude")

				yield self.input_keyword_required
				yield self.input_keyword_exclude

				yield Rule(line_style="heavy")
				
				with Horizontal(id="horizontal_groq"):
					self.checkbox_use_groq = Checkbox("Use Groq AI during scrapping", value=False, id="checkbox_use_groq")
					yield self.checkbox_use_groq

					with VerticalScroll(id="verticalscroll_groq"):
						self.input_user_skills = Input(placeholder = "Enter your professionnal skills", id = "input_user_skills", disabled=True)
						self.input_user_exclude_skills = Input(placeholder = "Excluded skills", id="input_user_exclude_skills", disabled=True)
						self.input_user_location = Input(placeholder = "Job location", id="input_user_location", disabled=True)
						yield self.input_user_skills
						yield self.input_user_exclude_skills
						yield self.input_user_location 

				with Horizontal(id = "horizontal_column_scrapping"):
					yield Button("START SCRAPPING", id="button_scrapping_start")
					yield Button("STOP SCRAPPING", id="button_scrapping_stop")
				#yield Button("remove children", id="button_remove_children")


			with VerticalScroll(id = "vertical_column_right"):
				with TabbedContent():
					with TabPane("SCRAPPING VIEW"):
						#yield Label("Linkedin posts")
						with Horizontal(id = "horizontal_scrapping_informations"):
							"""
							scrapping informations to display
								number of displayed posts
								number of saved post (in file)
								number of checked post in file (total)
							"""
							with Horizontal(id = "horizontal_scrapping_left"):
								self.label_counter_displayed = Label("",id="label_counter_displayed")
								self.label_counter_saved = Label("",id="label_counter_saved")
								self.label_counter_checked = Label("",id="label_counter_checked")
								yield self.label_counter_displayed
								yield self.label_counter_saved
								yield self.label_counter_checked
							with Vertical(id = "horizontal_scrapping_right"):
								yield Label("Maximum saved post(s) displayed",id="label_display_post_title")
								self.input_max_saved = Input(placeholder="Maximum saved post",type="integer",id="input_max_saved", value=str(self.user_data["MaxSavedDisplay"]))
								yield self.input_max_saved
						
						self.vertical_post_container = VerticalScroll(id = "vertical_post_container")
						yield self.vertical_post_container
					with TabPane("LOG VIEW"):
						self.listview_log = ListView(id = "listview_log")
						yield self.listview_log
						self.listview_log.border_title = "Application log"
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
		
		self.lock_log_file.acquire()
		#write log line
		with open("data/btmLog.log", "a", encoding="utf-8") as log_file:
			log_file.write("%s\n"%str(format_msg))
		#release the lock
		self.lock_log_file.release()
		
			#self.listview_log.append(ListItem(Label(str(traceback.format_exc()))))
		#update the log listview
		#check for the number of items already contained in the list
		#limit is set to 150?

		
		if len(self.listview_log.children)==50:
			self.listview_log.pop(0)

		if severity in ["success", "error"]:
			self.notify(str(message), timeout=3, severity="severity")
		
		#add the new item to the listview :)
		self.listview_log.append(ListItem(label))
		self.listview_log.scroll_end()
		

	#BINDINGS FUNCTION
	"""
	def action_binding_logs(self) -> None:
		self.query_one("#slidecontainer_right").toggle()
	"""
	

	def on_mount(self) -> None:
		self.display_message("Welcome in Bentham", "notification")
		self.display_message(" ","message",False)

		#create a title to the vertical column
		self.query_one("#vertical_post_container").border_title = "  LINKEDIN SAVED POST(S)  "
		
		#watch for theme changes
		self.watch(self.app, "theme", self.on_theme_change, init=False)
		#load user data
		self.load_user_data_function()
		self.load_scrapping_data_function()
		#update the interface
		self.update_lobby_informations()
		#launch the thread to read scrapping live
		self.thread_display_scrapping = threading.Thread(target=self.display_scrapping_function, args=(), daemon=True)
		self.thread_display_scrapping.start()

	def on_theme_change(self, old_value:str, new_value:str) -> None:
		# Called when app.theme changes.
		self.display_message(f"Application theme changed from [{old_value}] to [{new_value}]")
		#save the new application theme in the user data file
		self.user_data["ApplicationTheme"] = new_value
		self.save_user_data_function()

		

	def on_checkbox_changed(self, event:Checkbox.Changed) -> None:
		if event.checkbox.id == "checkbox_headless_browser":
			self.user_data["BrowserHeadless"] = self.checkbox_headless_browser.value
			self.save_user_data_function()
		if event.checkbox.id == "checkbox_custom_browser":
			self.input_custom_browser.disabled = not self.checkbox_custom_browser.value
			self.user_data["BrowserDifferent"] = self.checkbox_custom_browser.value
			self.save_user_data_function()
		if event.checkbox.id == "checkbox_use_groq":
			self.input_user_skills.disabled = not self.checkbox_use_groq.value
			self.input_user_exclude_skills.disabled = not self.checkbox_use_groq.value 
			self.input_user_location.disabled = not self.checkbox_use_groq.value
			self.user_data["LinkedinUseAI"] = self.checkbox_use_groq.value
			self.save_user_data_function()
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
		if event.input.id == "input_custom_browser":
			#check if there is something in the field
			if self.check_letter_function(self.input_custom_browser.value)==False:
				self.display_message("You must enter a filepath in this field","error")
				return
			elif os.path.isfile(self.input_custom_browser.value)==False:
				self.display_message("This filepath doesn't exists", "error")
				return
			else:
				#save the path in the user settings
				self.user_data["BrowserExecutable"] = self.input_custom_browser.value
				self.save_user_data_function()
				self.display_message("Custom browser executable saved", "success")
		if event.input.id in ["input_user_skills", "input_user_location", "input_user_exclude_skills"]:
			#get the content of the input field
			field_value_splited = self.query_one(f"#{event.input.id}").value.split(";")
			parsed_value_splited = []
			for element in field_value_splited:
				if self.check_letter_function(element)==True:
					parsed_value_splited.append(element)
			if event.input.id == "input_user_skills":
				self.user_data["LinkedinUserSkills"] = parsed_value_splited 
			elif event.input.id == "input_user_location":
				self.user_data["LinkedinUserLocation"] = parsed_value_splited
			else:
				self.user_data["LinkedinUserSkillsExclude"] = parsed_value_splited
			self.save_user_data_function()
			self.display_message("Groq prompting informations saved in user data", "success")

		"""
		if event.input.id == "input_user_skills":
			#split all user variables
			
			if self.check_letter_function(self.input_user_skills.value)==False:
				self.display_message("You must enter skills", "error")
				return
			user_skills = self.input_user_skills.value.split(";")
			self.user_data["LinkedinUserSkills"] = user_skills
			self.save_user_data_function()
			self.display_message("User skills saved successfully", "success")
		"""

		if event.input.id == "input_groq_apikey":
			#check if the key is empty or not
			if self.check_letter_function(self.input_groq_apikey.value)==False:
				self.display_message("You must enter an API Key to save", "error")
				return
			else:
				self.user_data["GroqAPIKey"] = self.input_groq_apikey.value
				self.save_user_data_function()
				self.display_message(f"Groq api key saved successfully : {self.user_data["GroqAPIKey"]}", "success")

		if event.input.id == "input_max_saved":
			self.user_data["MaxSavedDisplay"] = int(self.input_max_saved.value)
			self.save_user_data_function()
		if event.input.id in ["input_min_day_value", "input_max_day_value", "input_max_scrolling", "input_max_already_saved"]:
			if event.input.id == "input_min_day_value":
				self.user_data["MinDayValue"] = self.input_min_day_value.value
			if event.input.id == "input_max_day_value":
				self.user_data["MaxDayValue"] = self.input_max_day_value.value
				#self.display_message("changed")

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

		if event.input.id == "input_keyword_exclude":
			#split the keyword list
			splited_exclude = self.input_keyword_exclude.value.split(";")
			parsed_keyword_list = []
			for element in splited_exclude:
				if self.check_letter_function(element)==True:
					parsed_keyword_list.append(element)
			if len(parsed_keyword_list) != 0:
				self.user_data["KeywordExcluded"] = parsed_keyword_list
				self.save_user_data_function()
				self.display_message("Excluded word list saved", "success")
			else:
				self.display_message("No word detected in list", "error")
		
	def on_button_pressed(self, event:Button.Pressed) -> None:
		if event.button.id == "button_get_cookies":
			#install modal screens	
			self.install_screen(Modal_Bentham_AskCookies, name="Modal_Bentham_AskCookies")
			self.push_screen("Modal_Bentham_AskCookies")
			"""
			with self.suspend():
				value = self.get_linkedin_cookies_function()
				if value == True:
					#update password and username in user settings
					self.user_data["LinkedinMail"] = self.input_linkedin_username.value
					self.user_data["LinkedinPassword"] = self.input_linkedin_password.value
					self.save_user_data_function()
				os.system("pause")
			"""

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

