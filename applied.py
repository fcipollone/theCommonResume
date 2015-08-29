''' Controller for /employers{empID}/jobs/{jobID}'''
import cherrypy
import sys
import os.path
sys.stdout = sys.stderr # Turn off console output; it will get logged by Apache
import threading
import cherrypy
import os
import os.path
import math
import json
from collections import OrderedDict
import mysql.connector
from mysql.connector import Error
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))

class Applied(object):
	   exposed = True

    def __init__(self):
        self.db=dict()
        self.db['name']='theCommonResume'
        self.db['user']='root'
        self.db['host']='127.0.0.1'