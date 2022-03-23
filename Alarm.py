import smtplib
from email.message import EmailMessage

class Alarm():

    '''
    Diese Funktion ist für den Mailversand zuständig
    '''

    def sendAlarmMail(self_parameter=0, mail_login="", mail_to="", mail_password="", mail_server="", subject="", message=""):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] =  mail_login
        msg["To"] = mail_to
        msg.set_content(message)

        with smtplib.SMTP_SSL(mail_server, 465) as smtp:
            smtp.login(mail_login, mail_password)

            smtp.send_message(msg)