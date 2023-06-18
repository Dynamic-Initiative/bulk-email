import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from string import Template
import json
from dotenv import load_dotenv
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

load_dotenv()

emails = []

with open("./cert.json", "r") as f:
  emails = json.load(f)

s = smtplib.SMTP(host = 'dynamicini.org', port = 587)
s.starttls()
s.login(os.getenv("SENDER_MAIL"), os.getenv("SENDER_PASS"))

for email in emails:
  to_name = email["Adınız nedir?"]

  html = open("html/index.html").read()
  html = Template(open("html/index.html").read()).substitute(PERSON_NAME = to_name)
  msg = MIMEMultipart('related')

  msg['From'] = "info@dynamicini.org"
  msg['To'] = email["Emailiniz nedir?"]
  msg['Subject'] = "Dinamik Girişim Python Atölyesi Sertifika"

  ff = "certs/" + to_name + ".pdf"
  msg.attach(MIMEText(html, 'html'))
  with open(ff, "rb") as fil:
    part = MIMEApplication(
        fil.read(),
        Name = basename(ff)
    )
  part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(ff))
  msg.attach(part)

  s.send_message(msg)

  del msg

  print("Sent email to", to_name)
