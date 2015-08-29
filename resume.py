import apiutil
from apiutil import errorJSON
import sys
sys.stdout = sys.stderr # Turn off console output; it will get logged by Apache
import threading
import cherrypy
import os
import os.path
import json
from passlib.hash import md5_crypt
import mysql.connector
from mysql.connector import Error
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))
import logging
from config import conf
from pyvalidate import validate, ValidationException

class Resume(object):
	exposed = True

	def __init__(self):
		self.db = dict()
		self.db['name'] = 'theCommonResume'
		self.db['user'] = 'root'
		self.db['host'] = '127.0.0.1'
	
	def GET(self):
		output_format = cherrypy.lib.cptools.accept(['text/html'])
		if output_format == 'text/html':
			return env.get_template('resume-tmpl.html').render(
				base=cherrypy.request.base.rstrip('/') + '/'
            )




class StaticAssets(object):
    pass

if __name__ == '__main__':
    conf = {
        'global': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css'
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'js'
        }
    }
    cherrypy.tree.mount(Resume(), '/resume', {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    })
    cherrypy.tree.mount(StaticAssets(), '/', {
        '/': {
            'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css'
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'js'
        }
    })
    cherrypy.engine.start()
    cherrypy.engine.block()
else:
    application = cherrypy.Application(Resume(), None, conf)
