from kivy.uix.screenmanager import Screen
from database import db_connector, show_alert_dialog
from decouple import config
import random as r
import smtplib
import bcrypt
from email.message import EmailMessage
class ForgotPass(Screen):
    def __init__(self, **kw):
        super(ForgotPass, self).__init__(**kw)
    
    def send_mail(self):
        self.officer_email = self.ids.email.text
        my_db, my_cursor = db_connector()
        my_cursor.execute(f"select id from officer where email ='{self.officer_email}';")
        records = my_cursor.fetchall()
        if records:
            self.officer_id = records[0][0]
            msg = EmailMessage()
            msg['from'] = config("email")
            msg['to'] = self.officer_email
            msg['subject'] = "WIT TNP"
            self.otp=""
            for _ in range(6):
                self.otp+=str(r.randint(1,9))
            msg.set_content(f"Your OTP to reset password is {self.otp}. Please use it before switching to another page")
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
                    server.login(config("email"),config("email_password"))
                    server.send_message(msg)
                    show_alert_dialog(self,'OTP sent to mail id')
            except Exception:
                show_alert_dialog(self,'Couldnt send OTP due to an error')

        else:
            show_alert_dialog(self,'No such officer exists')
        
    def verify(self):
        if self.ids.otp.text == self.otp:
            self.ids.new_pass.disabled = False
            self.ids.confirm_pass.disabled = False
            self.ids.change.disabled = False
        else:
            show_alert_dialog(self,'Incorrect OTP')

    def change_password(self):
        if self.ids.new_pass.text == self.ids.confirm_pass.text:
            self.password = self.ids.new_pass.text
            hashed = bcrypt.hashpw(self.password.encode('ascii'),bcrypt.gensalt()).decode('ascii')
            my_db, my_cursor = db_connector()
            my_cursor.execute(f"update officer set password = '{hashed}' where id = {self.officer_id};")
            my_db.commit()
            show_alert_dialog(self,'Password changed successfully')
            self.manager.callback()
        else:
            show_alert_dialog(self,'Both password do not match')