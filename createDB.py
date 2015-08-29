#Use this script to create the database tables
#This script does NOT populate the tables with any data

import mysql.connector

#Define database variables
DATABASE_USER = 'root'
DATABASE_HOST = '127.0.0.1'
DATABASE_NAME = 'theCommonResume'

#Create connection to MySQL
cnx = mysql.connector.connect(user=DATABASE_USER, host=DATABASE_HOST)
cursor = cnx.cursor()

###################################
## Create DB if it doesn't exist ##
###################################

createDB = (("CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET latin1") % (DATABASE_NAME))
cursor.execute(createDB)

#########################
## Switch to feednd DB ##
#########################

useDB = (("USE %s") % (DATABASE_NAME))
cursor.execute(useDB)

###########################
## Drop all tables first ##
###########################
#Applied Jobs
dropTableQuery = ("DROP TABLE IF EXISTS applied")
cursor.execute(dropTableQuery) 

#Employer Jobs
dropTableQuery = ("DROP TABLE IF EXISTS jobs")
cursor.execute(dropTableQuery)  

#Applicant Work Experience
dropTableQuery = ("DROP TABLE IF EXISTS workExperience")
cursor.execute(dropTableQuery)

#Applicant School Info
dropTableQuery = ("DROP TABLE IF EXISTS schoolInfo")
cursor.execute(dropTableQuery)

#Employer Contact Info
dropTableQuery = ("DROP TABLE IF EXISTS employerInfo")
cursor.execute(dropTableQuery)

#Applicant Contact Info
dropTableQuery = ("DROP TABLE IF EXISTS applicantInfo")
cursor.execute(dropTableQuery)

#Employers
dropTableQuery = ("DROP TABLE IF EXISTS employers")
cursor.execute(dropTableQuery)

#Applicants
dropTableQuery = ("DROP TABLE IF EXISTS applicants")
cursor.execute(dropTableQuery)


########################
## Create tables next ##
########################

#applicants
createTableQuery = ('''CREATE TABLE applicants (
                    appID INT NOT NULL AUTO_INCREMENT,
                    name VARCHAR(45) CHARACTER SET utf8mb4  NOT NULL,
                    email VARCHAR(45)  CHARACTER SET utf8mb4 NOT NULL,
                    password VARCHAR(120)  CHARACTER SET utf8mb4 NOT NULL,
                    UNIQUE KEY (email) USING BTREE,
                    
                    PRIMARY KEY (appID))'''
                    )
cursor.execute(createTableQuery)

#employers
createTableQuery = ('''CREATE TABLE employers (
                    empID INT NOT NULL AUTO_INCREMENT,
                    name VARCHAR(45) CHARACTER SET utf8mb4  NOT NULL,
                    email VARCHAR(45)  CHARACTER SET utf8mb4 NOT NULL,
                    password VARCHAR(120)  CHARACTER SET utf8mb4 NOT NULL,
                    UNIQUE KEY (email) USING BTREE,
                    
                    PRIMARY KEY (empID))'''
                    )
cursor.execute(createTableQuery)

#applicantInfo
createTableQuery = ('''CREATE TABLE applicantInfo (
                        appID INT NOT NULL,
                        address NVARCHAR(100) NOT NULL,
                        city NVARCHAR(45) NOT NULL,
                        state NVARCHAR(20) NOT NULL,
                        zip NVARCHAR(10) NOT NULL,
                        phone NVARCHAR(20) NOT NULL,  

                        PRIMARY KEY(appID),
                        FOREIGN KEY(appID) REFERENCES applicants(appID) ON DELETE CASCADE);'''
                    )
cursor.execute(createTableQuery)

#employerInfo
createTableQuery = ('''CREATE TABLE employerInfo (
                        empID INT NOT NULL,
                        address NVARCHAR(100) NOT NULL,
                        city NVARCHAR(45) NOT NULL,
                        state NVARCHAR(20) NOT NULL,
                        zip NVARCHAR(10) NOT NULL,
                        phone NVARCHAR(20) NOT NULL,
                        website NVARCHAR(40) NOT NULL,

                        PRIMARY KEY(empID),
                        FOREIGN KEY(empID) REFERENCES employers(empID) ON DELETE CASCADE);'''
                    )
cursor.execute(createTableQuery)

#schoolInfo
createTableQuery = ('''CREATE TABLE schoolInfo (
                        schoolID INT AUTO_INCREMENT NOT NULL,
                        appID INT NOT NULL,
                        name NVARCHAR(100) NOT NULL,
                        city NVARCHAR(45) NOT NULL,
                        state NVARCHAR(20) NOT NULL,
                        major NVARCHAR(30) NOT NULL,
                        degree NVARCHAR(40) NOT NULL,
                        gpa NVARCHAR(3) NOT NULL,
                        gradDate NVARCHAR(10) NOT NULL,

                        PRIMARY KEY(schoolID),
                        FOREIGN KEY(appID) REFERENCES applicants(appID) ON DELETE CASCADE);'''
                    )
cursor.execute(createTableQuery)

#workExperience
createTableQuery = ('''CREATE TABLE workExperience (
                        workID INT AUTO_INCREMENT NOT NULL,
                        appID INT NOT NULL,
                        position NVARCHAR(100) NOT NULL,
                        company NVARCHAR(45) NOT NULL,
                        startdate NVARCHAR(20) NOT NULL,
                        enddate NVARCHAR(30) NOT NULL,
                        description NVARCHAR(400) NOT NULL,

                        PRIMARY KEY(workID),
                        FOREIGN KEY(appID) REFERENCES applicants(appID) ON DELETE CASCADE);'''
                    )
cursor.execute(createTableQuery)

#jobs
createTableQuery = ('''CREATE TABLE jobs (
                        jobID INT AUTO_INCREMENT NOT NULL,
                        empID INT NOT NULL,
                        name NVARCHAR(40) NOT NULL,
                        description NVARCHAR(400) NOT NULL,

                        PRIMARY KEY(jobID),
                        FOREIGN KEY(empID) REFERENCES employers(empID) ON DELETE CASCADE);'''
                    )
cursor.execute(createTableQuery)

#applied
createTableQuery = ('''CREATE TABLE applied(
                        appliedID INT AUTO_INCREMENT NOT NULL,
                        jobID INT NOT NULL,
                        appID INT NOT NULL,

                        PRIMARY KEY(appliedID),
                        FOREIGN KEY(jobID) REFERENCES jobs(jobID) ON DELETE CASCADE,
                        FOREIGN KEY(appID) REFERENCES applicants(appID) ON DELETE CASCADE);'''
                    )
cursor.execute(createTableQuery) 

#Commit the data and close the connection to MySQL
cnx.commit()
cnx.close()
