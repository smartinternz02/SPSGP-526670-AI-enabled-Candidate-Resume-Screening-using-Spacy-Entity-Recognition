import nltk
nltk.download('stopwords')

# Library to have connection to your gmail
import smtplib
# library to extract the entities form your resume
from pyresparser import ResumeParser


import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


creds = None
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = credentials.Credentials.from_authorized_user_file('token.json', SCOPES)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        flow = InstalledAppFlow.from_client_secrets_file(r'C:\Users\Chhavi Jain\OneDrive\Desktop\VS FILES\externship project\client_secret_668185049822-brj2cgur4dnrbvjuuk5c9grre7av8qf8.apps.googleusercontent.com.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())



#creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls ()

# Authentication
#s.login("jobmatch28@gmail.com","jobmatch1234")

# give a subject
SUBJECT = "Interview Call"
# skills requirement for Ai developer
python_skills = ["mL","ai","python","matplotlib","reression","algorithms","seabon","pandas","data analysis","keras","tensorflow", "artificial intelligence","data visualization","opencv"]
# skills requirement for Java developer
java_skills = []



# extract the skills from resume
data = ResumeParser(r'C:\Users\Chhavi Jain\OneDrive\Desktop\VS FILES\externship project\sample resume2.pdf').get_extracted_data()
print (data)
# grab the name
name = data ['name']
# grab the Email
email = data['email']
# grab the Skills
skills = data["skills"]
# lowercase the skills
actual_skills = [i.lower() for i in skills ]



# using list comprehension
# checking if string contains list element
Skills_matched = [ele for ele in actual_skills 
                if(ele in python_skills)]



# check the number of skills matched
if (len(Skills_matched) >= 4 ):
    
    print("he is eligible")
    # create a text that is to sent in an email
    TEXT = "Hello "+name + ",\n\n"+"Thanks for applying to the job post AI/ML Developer ."+"Your skils matches our requirement. Kindly let us "+"know the available time for initial round of interview. "+"\n\n\n\n Thanks and Regards, "+"\n\n Talent acquisition Team, \n\n Jobmatch"
    # send mail
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    # send the mail
    s.sendmail("jobmatch28@gmail.com",email, message)
    # quit the session
    s.quit()
else:
    print("sorry we cant process your candidature")
    
    TEXT = "Hello "+name + ",\n\n"+"Thanks for applying to the job post AI/ML Developer, "+"Your candidature is rejected. "+"\n\n\n\n Thanks and Regards, "+"\n\n Talent acquisition Team, \n\n Jobmatch"
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    s.sendmail("jobmatch28@gmail.com", email, message)
    s.quit()
