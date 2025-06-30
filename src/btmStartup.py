# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import traceback

from datetime import datetime

try:
	real_path = os.path.dirname(os.path.abspath(__file__))

	print("hello world")
	print(f"real current path : {real_path}")
except Exception as e:
	print(traceback.format_exc())
os.system("pause")