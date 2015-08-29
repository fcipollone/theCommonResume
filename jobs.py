''' Implements handler for /jobs
Imported from handler for /employers/{id} '''

import os, os.path, json, logging, mysql.connector

import cherrypy
from jinja2 import Environment, FileSystemLoader

from jobid import JobID

env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))

class Jobs(object):
    ''' Handles resources /jobs/{jobID}
        Allowed methods: GET, POST, PUT, DELETE '''
    exposed = True

    def __init__(self):
        self.id = JobID()
        self.db=dict()
        self.db['name']='theCommonResume'
        self.db['user']='root'
        self.db['host']='127.0.0.1'

    def getDataFromDB(self,id):
        cnx = mysql.connector.connect(
            user=self.db['user'],
            host=self.db['host'],
            database=self.db['name'],
        )
        cursor = cnx.cursor()
        qn="select name from employers where empID='%s'" % id
        cursor.execute(qn)
        empName=cursor.fetchone()[0]
        q="select jobID, name, description from jobs where empID='%s' order by name" % id
        cursor.execute(q)
        result=cursor.fetchall()
        return empName,result

    def GET(self, empID):
        ''' Return list of jobs for employer empID'''

        # Return data in the format requested in the Accept header
        # Fail with a status of 406 Not Acceptable if not HTML or JSON
        output_format = cherrypy.lib.cptools.accept(['application/json'])

        try:
            empName,result=self.getDataFromDB(empID)
        except mysql.connector.Error as e:
            logging.error(e)
            raise

        if output_format == 'text/html':
            return env.get_template('jobs-tmpl.html').render(
                eID=empID,
                eName=empName,
                jobs=result,
                base=cherrypy.request.base.rstrip('/') + '/'
            )
        else:
            data = [{
                'href': 'employers/%s/jobs/%s' % (empID, jobID),
                'name': name,
                'description': description
            } for jobID, name, description in result]
            return json.dumps(data, encoding='utf-8')

    def POST(self, **kwargs):
        result= "POST /employers/{empID}/jobs     ...     Jobs.POST\n"
        result+= "POST /employers/{empID}/jobs body:\n"
        for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data
        # Insert employer
        # Prepare response
        return result

    def OPTIONS(self,empID):
        return "<p>/employers/{empID}/jobs/ allows GET, POST, and OPTIONS</p>"
