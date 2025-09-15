# -*- coding: utf-8 -*-
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

from textual.app import App, ComposeResult
from textual.widgets import Sparkline, Tree, ProgressBar, Input, RadioSet, MarkdownViewer, RadioButton, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
#from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.screen import Screen, ModalScreen
from textual.await_complete import AwaitComplete
from textual.await_remove import AwaitRemove
from textual.binding import Binding, BindingType
# -*- coding: utf-8 -*-
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


from termcolor import *
from rich.console import Console
from rich import print as rprint
from time import sleep
from datetime import datetime 
from groq import Groq 
from groq import RateLimitError

from src.btmAI import BenthamGroq

import ast
import groq
import traceback
import pyperclip
import json
import re 
import argparse
import os 
import colorama

colorama.init()

class BenthamLINKEDIN:
	def get_linkedin_cookies_function(self):
		try:
			self.app.call_from_thread(self.app.display_message, "Trying to get linkedin cookies...")
			#username = self.input_linkedin_username.value
			#password = self.input_linkedin_password.value 

			#launch a browser with linkedin login page
			chrome_options = Options()
			chrome_options.add_argument("--window-size=1920,1080")
			chrome_options.add_argument("--disable-gpu")
			chrome_options.add_argument("--no-sandbox")
			chrome_options.add_argument("--disable-dev-shm-usage")
			#chrome_options.add_argument("--disable-logging")
			#chrome_options.add_argument("--log-level=3")
			#chrome_options.add_argument("--silent")

			"""
			if ("BrowserHeadless" in self.user_data) and (self.user_data["BrowserHeadless"]==True):
				chrome_options.add_argument("--headless")
			"""
			if ("BrowserExecutable" in self.app.user_data) and ("BrowserDifferent" in self.app.user_data):
				#replace the browser in driver settings
				if self.app.user_data["BrowserDifferent"]==True:	
					chrome_options.binary_location = self.app.user_data["BrowserExecutable"]
					#self.call_from_thread(self.display_message, f"Browser executable replaced : {self.user_data["BrowserExecutable"]}")
					self.app.call_from_thread(self.app.display_message, f"Browser executable replaced : {self.app.user_data["BrowserExecutable"]}")
					#chrome_options.binary_location = browser_path
					

					#GET THE DRIVER FOR CHROMIUM
					driver_path = os.path.normpath(os.path.join(os.getcwd(), "drivers/chromedriver-win64/chromedriver.exe"))
					if os.path.isfile(driver_path)==True:
						#self.call_from_thread(self.display_message, "Web browser driver found...", "notification")
						self.app.call_from_thread(self.app.display_message, "Web browser driver found...","notification")
						service = Service(driver_path)
						driver = webdriver.Chrome(options = chrome_options, service=service)
					else:
						#self.call_from_thread(self.display_message, "Impossible to find Web browser drivers", "error")
						self.app.call_from_thread(self.app.display_message, "Impossible to find web browser driver", "error")
						driver = webdriver.Chrome(options = chrome_options)
				else:
					driver = webdriver.Chrome(options = chrome_options)
			else:
				driver = webdriver.Chrome(options = chrome_options)

			#driver = webdriver.Chrome(options=chrome_options, service=service)
			#driver = webdriver.Chrome(options=chrome_options)
			driver.get("https://linkedin.com/login")

			clicked=False
			for i in range(1500):
				#self.app.call_from_thread(self.app.display_message, f"value : {self.login_done}")
				if self.login_done == None:
					self.app.call_from_thread(self.app.display_message, "Linkedin login canceled", "notification")
					return False
				if self.login_done==True:
					#get cookies from driver
					try:
						linkedin_cookies = driver.get_cookies()
						#display linkedin cookies
						#save linkedin cookies
						
						try:
							with open(os.path.join(os.getcwd(), "data/linkedin_cookies.json"), "w") as cookie_file:
								json.dump(linkedin_cookies, cookie_file, indent=4)
							self.app.user_data["LinkedinCookies"] = linkedin_cookies
							self.app.save_user_data_function()
							self.app.call_from_thread(self.app.display_message, "LINKEDIN COOKIES SAVED", "success")
							return True
						except Exception as e:
							#self.console.print("Impossible to save linkedin cookies in file\n%s"%traceback.format_exc(), style="error")
							self.app.call_from_thread(self.app.display_message, "Impossible to save linkedin cookies in file", "error")
							self.app.call_from_thread(self.app.display_message, traceback.format_exc(), "error", False)
							return False
					except Exception as e:
						self.app.call_from_thread(self.app.display_message, f"Impossible to get cookies from driver\n{traceback.format_exc()}", "error")
						return False

					clicked=True
					break

				sleep(1)

			self.app.call_from_thread(self.app.display_message, f"Login time limit has been reached", "error")
			return False
			#enter informations
			
			"""
			username_input = driver.find_element(By.ID, "username")
			password_input = driver.find_element(By.ID, "password")
			username_input.send_keys(username)
			password_input.send_keys(password)
			#find login button
			login_button = driver.find_element(By.CSS_SELECTOR, ".btn__primary--large.from__button--floating")
			login_button.click()
			#check for password error
			try:
				WebDriverWait(driver,3).until(
					EC.presence_of_element_located((By.ID, "error-for-password"))
				)
				self.display_message("Wrong password", "error")
				self.display_message("Impossible to get linkedin cookies from account", "error")
				#self.console.print("Wrong password", style="error")
				#self.console.print("Impossible to get linkedin cookies from account", style="error")
				return False
			except:
				#self.console.print("Connected to linkedin account...", style="success")
				self.display_message("Connected to linkedin account...", "notification")
				#try to get cookies from the linkedin page
				linkedin_cookies = driver.get_cookies()
				#display linkedin cookies
				#save linkedin cookies
				
				try:
					with open(os.path.join(os.getcwd(), "data/linkedin_cookies.json"), "w") as cookie_file:
						json.dump(linkedin_cookies, cookie_file, indent=4)
					self.user_data["LinkedinCookies"] = linkedin_cookies
				except Exception as e:
					#self.console.print("Impossible to save linkedin cookies in file\n%s"%traceback.format_exc(), style="error")
					self.display_message("Impossible to save linkedin cookies in file", "error")
					self.display_message(traceback.format_exc(), "error", False)
					return False
				else:
					#self.console.print("Linkedin cookies saved successfully", style="success")
					self.display_message("Linkedin cookies saved successfully", "success")
					return True
			"""
			#print(colored("PRESS <ENTER> WHEN YOU ARE CONNECTED TO YOUR LINKEDIN ACCOUNT TO SAVE COOKIES", "red"))
			#os.system("pause")

			"""
			try:
				linkedin_cookies = driver.get_cookies()
				#display linkedin cookies
				#save linkedin cookies
				
				try:
					with open(os.path.join(os.getcwd(), "data/linkedin_cookies.json"), "w") as cookie_file:
						json.dump(linkedin_cookies, cookie_file, indent=4)
					self.user_data["LinkedinCookies"] = linkedin_cookies
					self.display_message("LINKEDIN COOKIES SAVED", "success")
				except Exception as e:
					#self.console.print("Impossible to save linkedin cookies in file\n%s"%traceback.format_exc(), style="error")
					self.display_message("Impossible to save linkedin cookies in file", "error")
					self.display_message(traceback.format_exc(), "error", False)
					return False
			except Exception as e:
				self.display_message(f"Impossible to get cookies from driver\n{traceback.format_exc()}", "error")
				return False
			"""
		except Exception as e:
			self.app.call_from_thread(self.app.display_message, f"Error happened during thread\n{traceback.format_exc()}", "error")


	def thread_linkedin_scrapper(self):
		try:
			"""
			for i in range(50):
				if self.stop_thread_linkedin == False:
					self.call_from_thread(self.display_message, "thread stoped by intervention", "notification")
					break
				#self.call_from_thread(self.thread_display_message, "hello world")
				self.call_from_thread(self.display_message, "thread value : %s"%self.stop_thread_linkedin, "notification")
				sleep(0.2)
			"""
			#THIS BLOCK OF CODE CREATE THE WEBDRIVER AND TRY TO LOGIN USING LINKEDIN ACCOUNT!
			self.call_from_thread(self.display_message,"Linkedin scrapping initiated...", "notification")
			#try to create a web browser
			try:
				self.call_from_thread(self.display_message, "Creating web browser")
				#self.display_message("Trying to get linkedin cookies...")
				#launch a browser with linkedin login page
				chrome_options = Options()
				#DEFAULT BROWSER OPTIONS
				chrome_options.add_argument("--window-size=1920,1080")
				chrome_options.add_argument("--disable-gpu")
				if ("BrowserHeadless" in self.user_data) and (self.user_data["BrowserHeadless"]==True):
					chrome_options.add_argument("--headless")
				if ("BrowserExecutable" in self.user_data) and ("BrowserDifferent" in self.user_data):
					#replace the browser in driver settings
					if self.user_data["BrowserDifferent"]==True:	
						chrome_options.binary_location = self.user_data["BrowserExecutable"]
						self.call_from_thread(self.display_message, f"Browser executable replaced : {self.user_data["BrowserExecutable"]}")
					
				#browser_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
				driver_path = os.path.normpath(os.path.join(os.getcwd(), "drivers/chromedriver-win64/chromedriver.exe"))

				
				if os.path.isfile(driver_path)==True:
					self.call_from_thread(self.display_message, "Web browser driver found...", "notification")
					service = Service(driver_path)
					self.driver_linkedin_scrapping = webdriver.Chrome(options = chrome_options, service=service)
				else:
					self.call_from_thread(self.display_message, "Impossible to find Web browser drivers", "error")
					self.driver_linkedin_scrapping = webdriver.Chrome(options = chrome_options)
				
				connected=False
				for i in range(50):
					try:
						self.driver_linkedin_scrapping.get("https://linkedin.com")
					except WebDriverException as e:
						self.call_from_thread(self.display_message, "Impossible to access linkedin, please connect to internet", "error")
						sleep(5)
					else:
						connected=True
						break
						
				if connected==False:
					self.call_from_thread(self.display_message, "Impossible to access linkedin, program terminated", "error")
					exit()
				#get cookies
				#cookies = self.load_linkedin_cookies_function()
				if "LinkedinCookies" in self.user_data: 
					self.call_from_thread(self.display_message, "Trying to load cookies in driver...")
					try:
						#load cookies
						"""
						for cookie in self.user_data["LinkedinCookies"]:
							self.call_from_thread(self.display_message, f"  Cookie loaded [{list(self.user_data["LinkedinCookies"].keys()).index(cookie)} / {len(list(self.user_data["LinkedinCookies"].keys()))}]")
							self.driver_linkedin_scrapping.add_cookie(cookie)
						"""
						for i in range(len(self.user_data["LinkedinCookies"])):
							self.call_from_thread(self.display_message, f"  Cookie loaded [ {i} / {len(self.user_data["LinkedinCookies"])} ]")
							self.driver_linkedin_scrapping.add_cookie(self.user_data["LinkedinCookies"][i])
						self.driver_linkedin_scrapping.refresh()
						#enter user credentials and try to log in
						"""
						username_input = self.driver_linkedin_scrapping.find_element(By.ID, "username")
						password_input = self.driver_linkedin_scrapping.find_element(By.ID, "password")
						username_input.send_keys(self.user_data["LinkedinMail"])
						password_input.send_keys(self.user_data["LinkedinPassword"])
						login_button = self.driver_linkedin_scrapping.find_element(By.CSS_SELECTOR, ".btn__primary--large.from__button--floating")
						login_button.click()
						"""
						
					except Exception as e:
						self.call_from_thread(self.display_message, "Failed to load cookies in driver", "error")
						self.call_from_thread(self.display_message, traceback.format_exc(), "error")
						return
					else:
						self.call_from_thread(self.display_message, "Cookies loaded, driver refreshed", "success")
				else:
					self.call_from_thread(self.display_message, "Failed to load cookies from file", "error")
					self.call_from_thread(self.display_message, "Scrapping stoped", "notification")
					return
			except Exception as e:
				self.call_from_thread(self.display_message, "Failed to load linkedin driver", "error")
				self.call_from_thread(self.display_message, traceback.format_exc(), "error")
			else:
				self.call_from_thread(self.display_message, "Driver creation finished", "success")
				#sleep(5)
				#TRY TO CHANGE THE LINKEDIN DISPLAY MODE
				#get the value from the page
				self.update_display_mode_function()
				#LAUNCH THE FUNCTION WITH THE SCRAPPING LOOP
				self.scrapping_loop_function()

		except Exception as e:
			self.call_from_thread(self.display_message, f"Error happened during thread\n{traceback.format_exc()}", "error")
			#self.call_from_thread(self.display_message, traceback.format_exc())

		else:
			self.call_from_thread(self.display_message, "thread terminated", "success")

	def update_display_mode_function(self):
		try:
			self.call_from_thread(self.display_message, "Change display mode in linkedin...", "notification")
			sleep(2)
			#get the div trigger
			div_trigger = self.driver_linkedin_scrapping.find_element(By.CSS_SELECTOR, ".t-12.t-bold.mh1")
			#trigger div
			div_trigger.click()
			#try to get the unfolded div content
			div_content = self.driver_linkedin_scrapping.find_element(By.CSS_SELECTOR,".artdeco-dropdown__content--is-open")
			div_children = div_content.find_elements(By.CSS_SELECTOR, "*")
			#get li items in list
			page_displaymode_option_list = []
			for children in div_children:
				if children.tag_name == "li":
					page_displaymode_option_list.append(children)
					#self.call_from_thread(self.display_message, "option detected : %s"%children.text, "message")
			try:
				if "LinkedinDisplayMode" in self.user_data:
					value = self.user_data["LinkedinDisplayMode"]
				else:
					self.call_from_thread(self.display_message, "Linkedin display mode isn't saved in user data!\nDefault value set to 0")
					value=0
				page_displaymode_option_list[value].click()
				#page_displaymode_option_list[self.select_linkedin_displaymode.value].click()
			except Exception as e:
				self.call_from_thread(self.display_message, "Impossible to click on option to change display mode","error")
				self.call_from_thread(self.display_message, traceback.format_exc(), "error", False)
			else:
				self.call_from_thread(self.display_message, "Linkedin display mode changed", "success")
				#wait a bit sir 
				sleep(2)

		except Exception as e:
			self.call_from_thread(self.display_message, "Impossible to update the display mode in linkedin", "error")
			self.call_from_thread(self.display_message, traceback.format_exc(), "error", False)
		else:
			self.call_from_thread(self.display_message, "Changing display mode function terminated", "success")

	def scrapping_loop_function(self):
		#create the wait long variable
		self.wait_long = WebDriverWait(self.driver_linkedin_scrapping, 10)
		self.call_from_thread(self.display_message, "Starting to get linkedin data from feed...", "notification")
		"""
		refresh conditions
		- limit date is reached
		- limit number of scrolling iteration is reached
		- limit number of 'already saved post' is reached
		"""

		#create all counter variables
		#i is the max loop variable! don't change it
		counter_max_day = 0
		counter_max_scrolling = 0
		counter_max_checked = 0
		counter_max_saved = 0
		for i in range(500):
			#stop thread condition
			if self.stop_thread_linkedin==False:
				self.call_from_thread(self.display_message, "User stoped the thread...", "notification")
				try:
					self.driver_linkedin_scrapping.quit()
				except Exception as e:
					self.display_message("Impossible to kill driver", "error")
					self.display_message(traceback.format_exc(), "error")
				else:
					self.display_message("Driver killed successfully", "success")
				return

			self.call_from_thread(self.display_message, "="*90, "notification")
			self.call_from_thread(self.display_message, "New loop start...", "notification")
			self.call_from_thread(self.display_message, "="*90, "notification")

			self.driver_linkedin_scrapping.execute_script("window.scrollTo(0,document.body.scrollHeight);")
			self.wait_long.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-shared-update-v2")))
			sleep(2)

			#get the list of the post
			#get content of the page
			list_post = self.driver_linkedin_scrapping.find_elements(By.CSS_SELECTOR, "div.feed-shared-update-v2")
			list_button = self.driver_linkedin_scrapping.find_element(By.CSS_SELECTOR, 'button.feed-shared-control-menu__trigger.artdeco-button.artdeco-button--tertiary.artdeco-button--muted.artdeco-button--1.artdeco-button--circle.artdeco-dropdown__trigger.artdeco-dropdown__trigger--placement-bottom.ember-view')

			for post in list_post:
				
				if self.stop_thread_linkedin==False:
					self.call_from_thread(self.display_message, "User stoped the thread...", "notification")
					try:
						self.driver_linkedin_scrapping.quit()
					except Exception as e:
						self.display_message("Impossible to kill driver", "error")
						self.display_message(traceback.format_exc(), "error")
					else:
						self.display_message("Driver killed successfully", "success")
					return

				#self.call_from_thread(self.display_message, f"Checking new post content → {post._id}", "notification")
				#CHECK IF THE POST HAS ALREADY BEEN CHECKED
				post_id = post.get_attribute("data-urn") or post.text[:50]
				if post_id in self.linkedin_post_checked:
					#self.call_from_thread(self.display_message, "Already checked | Post skipped → %s"%post_id, "message")
					continue
				else:
					self.linkedin_post_checked.append(post_id)
				
				#self.call_from_thread(self.display_message,"Display post content","notification")
				#self.call_from_thread(self.display_message, "POST ID → %s"%post_id,"notification")
				#self.call_from_thread(self.display_message, str(post))
				#post_title = post.find_elements(By.CSS_SELECTOR, "span[aria-hidden='true']")[0]
				post_text_list_element = post.find_elements(By.CSS_SELECTOR, "span[dir='ltr']")
				post_text_list = []
				post_author = post.find_elements(By.CSS_SELECTOR, "span[aria-hidden='true']")[0]

				self.call_from_thread(self.display_message, "Post author : %s"%post_author.text)
				self.call_from_thread(self.display_message, "\n","message",False)

				for element in post_text_list_element:
					#self.call_from_thread(self.display_message,str(element.text),"message",False)
					post_text_list.append(element.text)
				#join post_text_list
				post_text = "\n".join(post_text_list)

				self.call_from_thread(self.display_message, f"\nLinkedin post content\n{post_text}", "message", False)
				#CHECK FOR CONTENT IN POST
				if self.user_data["LinkedinUseAI"]==False:
					#check if keyword are in the post text
					if self.check_post_content_function(post_text)==False:
						self.call_from_thread(self.display_message, "Post skipped", "notification")
						continue
					elif self.check_post_content_function(post_text)==True:
						self.call_from_thread(self.display_message, "Keyword detected in post", "success")
					else:
						self.call_from_thread(self.display_message, "Impossible to check for keywords in post", "warning")
				else:
					#PROMPT THE GROQ CLASS
					try:
						callinggroq = BenthamGroq(api_key = self.user_data["GroqAPIKey"], post_content=post_text, user_skills = self.user_data["LinkedinUserSkills"], user_location = self.user_data["LinkedinUserLocation"], user_skills_excluded = self.user_data["LinkedinUserSkillsExclude"])
						callinggroq_output = callinggroq.run()
					except RateLimitError:
						self.call_from_thread(self.display_message, f"Token limit reached, You can't use Groq AI right now\nPlease try again later", "error")
						self.call_from_thread(self.display_message, '"Use Ai" value changed → Switched to keyword detection', "notification")
						#try to disable enable and change settings
						self.user_data["LinkedinUseAI"]=False 
						#change checkbox value
						try:
							self.checkbox_use_groq.value=False 
						except AttributeError:
							pass
						#save user settings
						self.save_user_data_function()
						#start the loop over after disabling ai model
						continue
					except Exception as e:
						self.call_from_thread(self.display_message, f"Impossible to call AI for scrapping\n{traceback.format_exc()}", "error")
						return
					else:
						#self.call_from_thread(self.display_message, f"Output from AI\n{callinggroq_output}")
						#try to convert the returned dictionnary into real python dictionnary
						try:
							groq_output_dictionnary = ast.literal_eval(callinggroq_output)
							#create assertion for dictionnary
							assert type(groq_output_dictionnary) == dict, f"Groq output isn't a python dictionnary\n{groq_output_dictionnary}\n{type(groq_output_dictionnary)}"
							assert "is_matching" in groq_output_dictionnary, "Impossible to access data in dictionnary"
							assert "job_searched" in groq_output_dictionnary, "Impossible to access data in dictionnary"
											 
						except Exception as e:
							self.call_from_thread(self.display_message, callinggroq_output)
							#self.call_from_thread(self.display_message, groq_output_dictionnary)
							self.call_from_thread(self.display_message, f"Failed to convert groq output into dictionnary\n{callinggroq_output}\n{traceback.format_exc()}", "error")
							continue
						except AssertionError as e:
							self.call_from_thread(self.display_message, e, "error")
							continue
						else:
							#check informations in dictionnary
							self.call_from_thread(self.display_message, f"Output from GROQ\nPosition researched : {groq_output_dictionnary["job_searched"]}\nPost matching skills : {groq_output_dictionnary["is_matching"]}")
							if groq_output_dictionnary["is_matching"]==False:
								self.call_from_thread(self.display_message, "This post doesn't match with your request", "notification")
								continue
							else:
								self.call_from_thread(self.display_message, "Matching post detected", "success")
				#GET SHARED POST CONTENT
				post_shared = post.find_elements(By.CSS_SELECTOR, "div.feed-shared-update-v2__update-content-wrapper")
				post_shared_text = None
				if len(post_shared) != 0:
					post_shared = post_shared[0]
					#try to find the text contained inside of the post_shared variable
					post_shared_text = post_shared.find_elements(By.CSS_SELECTOR, "span[dir='ltr']")
					for i in range(len(post_shared_text)):
						post_shared_text[i] = post_shared_text[i].text

					post_text_shared_combined = "\n".join(post_shared_text)
					#self.call_from_thread(self.display_message, "Shared content\n%s"%post_shared_text[i], "notification")

				#GET THE LINK OF THE POST
				post_link = self.get_post_link_function(post)
				if post_link != False:
					#GET THE POSTING DATE
					post_date = self.get_linkedin_post_date_function(post_link)
					if post_date != None:
						self.call_from_thread(self.display_message, "Date detected in post : %s"%str(post_date),"success")
						#self.call_from_thread(self.display_message, str(type(post_date)), "message")
						post_date_converted = datetime.strptime((post_date.replace(" (UTC)", "")),"%a, %d %b %Y %H:%M:%S")
						delta = (datetime.now()-post_date_converted).days

						self.call_from_thread(self.display_message, "Converted date : %s"%str(post_date_converted))
						self.call_from_thread(self.display_message, "Delta : %s"%str(delta))

						#check if the delta in days is contained in interval
						if ("MinDayValue" in self.user_data) and ("MaxDayValue" in self.user_data):
							if (delta >= int(self.user_data["MinDayValue"])) and (delta <= int(self.user_data["MaxDayValue"])):
								self.call_from_thread(self.display_message, "Interval value are matching...","message")
								#create a unique identifier for this post
								post_timestamp = int(post_date_converted.timestamp() * 1000)
								self.call_from_thread(self.display_message, "Unique timestamp created for this post : %s"%post_timestamp)
								#check if the timestamp is not already in table
								if post_timestamp not in self.linkedin_scrapping_table:
									#create the data dictionnary for this post
									post_data_table = {
										"postIdentifier":post_timestamp,
										"postDate":str(post_date_converted),
										"postAuthor":post_author.text,
										"postContent":post_text,
										"postLink":post_link
									}
									if post_shared_text != None:
										post_data_table["postSharedContent"] = post_shared_text
									#add the post in the table
									self.linkedin_scrapping_table[post_id] = post_data_table
									self.call_from_thread(self.display_message, "Post saved in scrapping dictionnary\n", "success")
									#call saving function
									#self.save_scrapping_function()
								else:
									self.call_from_thread(self.display_message, "POST ALREADY DETECTED IN SCRAPPING DATA → SKIPPED", "error")
									counter_max_saved+=1
							else:
								self.call_from_thread(self.display_message, "Interval values are not matching", "warning")
								self.call_from_thread(self.display_message, "Skipping saving", "warning")
						else:
							self.call_from_thread(self.display_message, "Missing settings to define if post match time range", "error")
				self.scrapping_data = {
					"LinkedinScrapping":self.linkedin_scrapping_table,
					"LinkedinCheckedPost":self.linkedin_post_checked
				}
				self.save_scrapping_function()
				self.call_from_thread(self.display_message, "\n\n", "message", False)
				"""
				for post_text in list_post_text:
					self.call_from_thread(self.display_message, str(post_text.text))
				"""
				"""
				post_title = post.find_elements(By.CSS_SELECTOR, "span[aria-hidden='true']")[0]
				post_text = post.find_elements(By.CSS_SELECTOR, "span[dir-'ltr']")
				self.call_from_thread(self.display_message, "POST TITLE→%s\nPOST CONTENT→%s"%(post_title, post_text),False)
				"""
			self.driver_linkedin_scrapping.execute_script("window.scrollTo(0,document.body.scrollHeight);")
			self.wait_long.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-shared-update-v2")))
			sleep(2)

			counter_max_scrolling += 1
		self.call_from_thread(self.display_message, "Scrapping limit reached → Process stoped")
		return


	def check_post_content_function(self, content):
		#get the keywords to check in settings
		self.call_from_thread(self.display_message, content)
		if ("KeywordExcluded" in self.user_data) and (type(self.user_data["KeywordExcluded"])==list):
			for keyword in self.user_data["KeywordExcluded"]:
				if (keyword.upper() in content) or (keyword.lower() in content) or (keyword.capitalize() in content):
					self.call_from_thread(self.display_message, f"  Excluded keyword found : {keyword}", "error")
					return False

		if ("KeywordRequired") not in self.user_data:
			self.call_from_thread(self.display_message, "Impossible to check for keywords","warning")
			return None

		checking_status=False
		for keyword_list in self.user_data["KeywordRequired"]:
			for keyword in keyword_list:
				if (keyword.upper() in content) or (keyword.lower() in content) or (keyword.capitalize() in content):
					self.call_from_thread(self.display_message, f"  Keyword detected : {keyword}","success")
					checking_status=True
				#else:
				#self.call_from_thread(self.display_message, f'  Keyword not detected : {keyword}', "message")


		return checking_status

	def get_post_link_function(self,post):
		try:
			#clean the content of the copy 
			pyperclip.copy("nothing copied")
			post_button = WebDriverWait(post, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.feed-shared-control-menu__trigger')))
			ActionChains(self.driver_linkedin_scrapping).move_to_element(post_button).perform()
			WebDriverWait(self.driver_linkedin_scrapping,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.feed-shared-control-menu__trigger')))
			post_button.click()
			post_div = post.find_element(By.CSS_SELECTOR, 'div.feed-shared-control-menu__content')
			menu_option = WebDriverWait(self.driver_linkedin_scrapping, 8).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'feed-shared-control-menu__content')]//div[@role='button']")))			
			menu_option[1].click()
			post_link = pyperclip.paste()
			self.call_from_thread(self.display_message, "Post link : %s"%post_link)
		except Exception as e:
			self.call_from_thread(self.display_message, "Impossible to get post link", "error")
			self.call_from_thread(self.display_message, traceback.format_exc(), "error")
			self.call_from_thread(self.display_message, "Posting date detection skipped", "error")
			return False
		else:
			return post_link


	def get_linkedin_post_date_function(self,url):
		post_id = self.get_post_id(url)
		if post_id:
			unix_timestamp = self.extract_unix_timestamp(post_id)
			human_date_format = self.unix_timestamp_to_human_date(unix_timestamp)
			return human_date_format
		return None

	def get_post_id(self,url):
		regex = r"activity-([0-9]+)"
		match = re.search(regex, url)
		if match:
			return match.group(1)
		return None


	def extract_unix_timestamp(self,post_id):
		as_binary = format(int(post_id), "064b")
		first42_chars = as_binary[:42]
		timestamp = int(first42_chars, 2)
		return timestamp


	def unix_timestamp_to_human_date(self,timestamp):
		date_object = datetime.utcfromtimestamp(timestamp / 1000)
		human_date_format = date_object.strftime("%a, %d %b %Y %H:%M:%S (UTC)")
		return human_date_format




	def load_linkedin_cookies_function(self):
		self.call_from_thread(self.display_message, os.getcwd(), "message")

		if "LinkedinCookies" not in self.user_data:
			self.call_from_thread(self.display_message, "Impossible to get linkedin cookies in settings", "error")
			return False
		else:
			return True
		"""
		if os.path.isfile(os.path.join(os.getcwd(), "data/linkedin_cookies.json"))==False:
			self.call_from_thread(self.display_message, "Cookie not saved in file", "error")
			return None
		else:
			try:
				with open("data/linkedin_cookies.json", "r") as read_file:
					cookies = json.load(read_file)
			except Exception as e:
				self.call_from_thread(self.display_message, "Impossible to load cookies", "error")
				return None
			else:
				self.call_from_thread(self.display_message, "Cookies retrieved from file", "success")
				return cookies
		"""
