# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import traceback
import threading

import colorama
import pyfiglet


class BenthamUTILITY:
	def check_letter_function(self, content):
		letter = "abcdefghijklmnopqrstuvwxyz"
		figure = "0123456789"
		capital = letter.upper()

		list_letter = list(letter)
		list_capital = list(capital)
		list_figure = list(figure)

		try:
			list_content = list(content)
		except Exception as e:
			return False

		for i in range(len(list_content)):
			if (list_content[i] in list_letter) or (list_content[i] in list_figure) or (list_content[i] in list_capital):
				return True
		return False