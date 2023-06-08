import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from string import Template
import json
from dotenv import load_dotenv
import os

load_dotenv()

emails = []

with open("./mails.json", "r") as f:
  emails = json.load(f)

s = smtplib.SMTP(host = 'dynamicini.org', port = 587)
s.starttls()
s.login(os.getenv("SENDER_MAIL"), os.getenv("SENDER_PASS"))

fp = open('html/images/DI_LOGO_beyaz.png', 'rb')
beyazDI = MIMEImage(fp.read())
beyazDI.add_header('Content-ID', '<beyazDI>')
fp.close()

fp = open('html/images/di_logo_krmz.png', 'rb')
kirmiziDI = MIMEImage(fp.read())
kirmiziDI.add_header('Content-ID', '<kirmiziDI>')
fp.close()

for email in emails:
  to_name = email["Adınız nedir?"]

  html = open("html/index.html").read()
  html = Template(open("html/index.html").read()).substitute(PERSON_NAME = to_name)
  msg = MIMEMultipart('related')

  msg['From'] = "info@dynamicini.org"
  msg['To'] = email["Emailiniz nedir?"]
  msg['Subject'] = "Dinamik Girişim Python Atölyesi İkinci Ders"

  msg.attach(MIMEText(html, 'html'))

  msg.attach(beyazDI)
  msg.attach(kirmiziDI)

  s.send_message(msg)

  del msg

  print("Sent email to", to_name)