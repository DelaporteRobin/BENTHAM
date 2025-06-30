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

		self.display_message("Updating informations done...", "success")