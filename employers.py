''' /employers resource for feednd.com
This is run as a WSGI application through CherryPy and Apache with mod_wsgi
Author: Jesus A. Izaguirre, Ph.D.
Date: Feb. 17, 2015
Web Applications'''
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
#from employerid import EmployerID
from jobs import Jobs
import logging
from config import conf


''' Controller for /employers/{id}
    Imported from handler for /employers '''
class EmployerID(object):
    ''' Handles resource /employers/{id} 
        Allowed methods: GET, PUT, DELETE, OPTIONS '''
    exposed = True

    def __init__(self):
        self.jobs = Jobs()
        self.db = dict()
        self.db['name']='theCommonResume'
        self.db['user']='root'
        self.db['host']='127.0.0.1'
        self.info = dict()
        self.xtra = dict()

    def getDataFromDB(self,empID):
        try:
            cnx = mysql.connector.connect(
                user=self.db['user'],
                host=self.db['host'],
                database=self.db['name'],
            )
            cursor = cnx.cursor()
            q="select empID, name, email from employers where empID = %s;" % empID
            cursor.execute(q)
        except Error as e:
            logging.error(e)
            raise

        self.data = []
        for (empID, name, email) in cursor:
            self.data.append({
                         'name':name,
                         'email':email
                         })
            self.info[empID] = (name, email)
        try:
            cnx = mysql.connector.connect(
                user=self.db['user'],
                host=self.db['host'],
                database=self.db['name'],
            )
            cursor = cnx.cursor()
            q="select empID, address,city,state,zip,phone,website from employerInfo where empID = %s;" % empID
            cursor.execute(q)
        except Error as e:
            logging.error(e)
            raise
        for (empID,address,city,state,zip,phone,website) in cursor:
            self.xtra[empID] = (address, city, state, zip, phone, website)

    def GET(self, empID):
        output_format = cherrypy.lib.cptools.accept(['application/json'])

        self.getDataFromDB(empID)
        
        return json.dumps(self.xtra, encoding='utf-8')

    def PUT(self,empID):
        dat = cherrypy.request.body.read()
        mydict = json.loads(dat)
        try:
            cnx = mysql.connector.connect(
                user=self.db['user'],
                host=self.db['host'],
                database=self.db['name'],
            )
            cursor = cnx.cursor()
            fakepass = "fake password"
            comp = mydict['name']
            email = mydict['email']
            q= "UPDATE employers SET name=" + "'" + comp + "',email =" + "'" + email + "',password='" + fakepass + "' WHERE empID = " + empID + ";"
            print q
            cursor.execute(q)
        except Error as e:
            logging.error(e)
            raise
        try:
            cnx.commit()
            cnx.close()
        except Error as e:
            #Failed to insert orderItem
            print "mysql error: %s" % e
        result = {'result' : 'success'}
        return json.dumps(result)

    def DELETE(self,empID):
        try:
            cnx = mysql.connector.connect(
                user=self.db['user'],
                host=self.db['host'],
                database=self.db['name'],
            )
            cursor = cnx.cursor()
            q = "delete * from employers where empID = 3;"
            cursor.execute("delete from employers where empID = 3;")
        except Error as e:
            logging.error(e)
            raise
        try:
            cnx.commit()
            cnx.close()
        except Error as e:
            #Failed to insert orderItem
            print "mysql error: %s" % e
        result = {'result' : 'success'}
        return json.dumps(result)
        
    def OPTIONS(self, empID):
        ''' Allows GET, PUT, DELETE, OPTIONS '''
        #Prepare response
        return "<p>/employers/{id} allows GET, PUT, DELETE, and OPTIONS</p>"



class Employers(object):
    ''' Handles resource /employers
        Allowed methods: GET, POST, OPTIONS '''
    exposed = True

    def __init__(self):
        self.id=EmployerID()
        self.db = dict()
        self.db['name']='theCommonResume'
        self.db['user']='root'
        self.db['host']='127.0.0.1'
        self.info = dict()
        self.xtra = dict()

    def _cp_dispatch(self,vpath):
            print "Employers._cp_dispatch with vpath: %s \n" % vpath
            if len(vpath) == 1: # /employers/{id}
                cherrypy.request.params['empID']=vpath.pop(0)
                return self.id
            if len(vpath) == 2: # /employers/{id}/jobs
                cherrypy.request.params['empID']=vpath.pop(0)
                vpath.pop(0) 
                return self.id.jobs
            if len(vpath) == 3: # /employers/{id}/jobs/{jobID}
                cherrypy.request.params['empID']=vpath.pop(0)
                vpath.pop(0)
                cherrypy.request.params['jobID']=vpath.pop(0)
                return self.id.jobs.id   

            return vpath

    def getDataFromDB(self):
        try:
            cnx = mysql.connector.connect(
                user=self.db['user'],
                host=self.db['host'],
                database=self.db['name'],
            )
            cursor = cnx.cursor()
            q="select empID, name, email from employers;"
            cursor.execute(q)
        except Error as e:
            logging.error(e)
            raise
        self.data = []
        for (empID, name, email) in cursor:
            self.data.append({
                         'name':name,
                         'email':email
                         })
            self.info[empID] = (name, email)
        try:
            cnx = mysql.connector.connect(
                user=self.db['user'],
                host=self.db['host'],
                database=self.db['name'],
            )
            cursor = cnx.cursor()
            q="select empID, address,city,state,zip,phone,website from employerInfo"
            cursor.execute(q)
        except Error as e:
            logging.error(e)
            raise
        for (empID,address,city,state,zip,phone,website) in cursor:
            self.xtra[empID] = (address, city, state, zip, phone, website)


    def GET(self):
        output_format = cherrypy.lib.cptools.accept(['text/html', 'application/json'])

        self.getDataFromDB()

        if output_format == 'text/html':
            return env.get_template('employers-tmpl.html').render(
                employers=self.info,
                info=self.xtra,
                base=cherrypy.request.base.rstrip('/') + '/'
            )
        else:
            return json.dumps(self.data, encoding='utf-8')

    def POST(self):
        dat = cherrypy.request.body.read()
        mydict = json.loads(dat)
        try:
            cnx = mysql.connector.connect(
                user=self.db['user'],
                host=self.db['host'],
                database=self.db['name'],
            )
            cursor = cnx.cursor()
            fakepass = "fake password"
            comp = mydict['name']
            email = mydict['email']
            q="insert into employers (name, email, password) values ("
            q += "'" + comp + "'" +  ',' + "'" + email + "'" + ',' + "'" +  fakepass + "'" + ');'
            print q
            cursor.execute(q)
        except Error as e:
            logging.error(e)
            raise
        try:
            cnx.commit()
            cnx.close()
        except Error as e:
            #Failed to insert orderItem
            print "mysql error: %s" % e
        result = {'result' : 'success'}
        return json.dumps(result)

    def OPTIONS(self):
        ''' Allows GET, POST, DELETE OPTIONS '''
        #Prepare response
        return "<p>/restaurants/ allows GET, POST, and OPTIONS</p>"

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
    cherrypy.tree.mount(Employers(), '/employers', {
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
    application = cherrypy.Application(Employers(),None,conf)

