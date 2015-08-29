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

class JobID(object):
    ''' Handles resources /jobs/{empID}/{id}
        Allowed methods: GET, PUT, DELETE, OPTIONS '''
    exposed = True

    def __init__(self):
        self.db=dict()
        self.db['name']='theCommonResume'
        self.db['user']='root'
        self.db['host']='127.0.0.1'

    def getDataFromDB(self,empID,jobID):
        cnx = mysql.connector.connect(
            user=self.db['user'],
            host=self.db['host'],
            database=self.db['name'],
        )
        cursor = cnx.cursor()
        qn="select name from employers where empID='%s'" % empID
        cursor.execute(qn)
        empName=cursor.fetchone()[0]
        q="select name from jobs where jobID='%s'" % jobID
        cursor.execute(q)
        name_result=cursor.fetchone()
        q="select description from jobs where jobID='%s'" % jobID
        cursor.execute(q)
        description_result=cursor.fetchone()
        return empName,name_result,description_result

    def GET(self,empID,jobID):
        output_format = cherrypy.lib.cptools.accept(['text/html', 'application/json'])

        empName,name_result,description_result = self.getDataFromDB(empID,jobID)

        if output_format == 'text/html':
            return env.get_template('job-tmpl.html').render(
                emp_name = empName,
                job_name=name_result[0],
                description=description_result[0],
                base=cherrypy.request.base.rstrip('/') + '/'
            )
        else:
            return "GET /employers{empID=%s}/jobs/{jobID=%s}}   ...   JobID.GET" % (empID,jobID)

    def POST(self, empID, jobID):
        print "jobID",jobID
        output_format = cherrypy.lib.cptools.accept(['application/json'])
        try:
            cnx = mysql.connector.connect(
                user=self.db['user'],
                host=self.db['host'],
                database=self.db['name'],
            )
            cursor = cnx.cursor()

        except Error as e:
            print e

        appID = 1
        qn=str(jobID) + "insert into applied (jobID, appID) values (%s,%s);" % (jobID, appID)
        try:
            cursor.execute(qn)
            cnx.close()
        except Error as e:
            print e
        print qn
        # Validate form data
        # Insert or update restaurant
        # Prepare response
        result = {}
        result['jobID'] = jobID
        result['appID'] = appID
        result['request'] = qn
        return json.dumps(result)

    def DELETE(self, empID, jobID):
        #Validate id
        #Delete restaurant
        #Prepare response
        return "DELETE /employers{empID=%s}/jobs/{jobID=%s}   ...   JobID.DELETE" % (empID,jobID)

    def OPTIONS(self, empID, jobID):
        #Prepare response
        return "<p>/employers{empID}/jobs/{jobID} allows GET, PUT, DELETE, and OPTIONS</p>"

