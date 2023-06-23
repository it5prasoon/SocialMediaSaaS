from smtplib import SMTP
# from email.encoders import encode_base64
# from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ as os_environ
import secrets
import firebase_admin
from firebase_admin import db

cred_obj1 = firebase_admin.credentials.Certificate('api_database.json')
app1 = firebase_admin.initialize_app(cred_obj1, {'databaseURL': 'https://toornamnet-bot-default-rtdb.firebaseio.com/'},
                                     name='app1')
ref1 = db.reference('/', app1)


def convert_username_firebase(text):
    res = ''
    for x in text:
        res += str(ord(x)) + '-'
    return res[:-1]


def create_key():
    return secrets.token_urlsafe(16)


def send_email(email_receiver):
    fromaddr = "prasoonk187@gmail.com"  # USE YOUR EMAIL ID HERE
    toaddr = email_receiver

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = 'TEST API KEY'

    # string to store the body of the mail
    key = create_key()
    body = f'Your API Key is {key}'
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    # filename = "Resume.docx"
    # attachment = open(f"{pathlib.Path(__file__).parent.resolve()}\Manish Kothary -Chief Technology Officer Resume.DOCX", "rb")
    # attachment = open(f"Manish Kothary -Chief Technology Officer Resume.DOCX", "rb")
    # instance of MIMEBase and named as p
    # p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    # p.set_payload((attachment).read())

    # encode into base64
    # encode_base64(p)

    # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    # msg.attach(p)

    # creates SMTP session
    s = SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    password = os_environ.get("GMAIL_APP_PASSWORD")
    s.login(fromaddr, password)  # USE YOUR OWN APP PASSWORD; DIFFERENT FROM YOUR GMAIL PASSOWRD

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
    print('A MAIL HAS BEEN SENT')
    ref1.child(convert_username_firebase(email_receiver)).update({'key': key, 'subscription_type': 1})
    # terminating the session
    s.quit()
