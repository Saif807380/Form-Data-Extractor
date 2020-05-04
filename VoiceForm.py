import pdfkit
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import render_template

class VoiceForm:

    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    sender_address = 'team6nn@gmail.com'
    sender_pass = 'yehHackathontohHuahiNahi'

    def __init__(self):
        print("")

    def generatePDF(self,form):
        path = './voiceforms/' + form['email'] + '.pdf'
        rendered = render_template('pdf_template.html',form=form)
        pdfkit.from_string(rendered,path,configuration=self.__class__.config) 
        return path

    def sendEmail(self,reciever_address,attach_file_name):
        message = MIMEMultipart()
        message['From'] = self.__class__.sender_address
        message['To'] = reciever_address
        message['Subject'] = 'A copy of your voice form response.'
        mail_content = """
            blah blah blah
        """
        message.attach(MIMEText(mail_content, 'plain'))
        attach_file = open(attach_file_name, 'rb') 
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) 
        payload.add_header('Content-Disposition', 'attachment; filename="%s.pdf"' % reciever_address)
        message.attach(payload)
        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls() 
        session.login(self.__class__.sender_address, self.__class__.sender_pass) 
        text = message.as_string()
        session.sendmail(self.__class__.sender_address, reciever_address, text)
        session.quit()
        print('Mail Sent')