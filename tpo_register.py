from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from database import show_alert_dialog
from login import Login
import flags
import bcrypt
import re
import random as r
import smtplib
from email.message import EmailMessage
from decouple import config
from mysql.connector.errors import InterfaceError

class TpoRegister(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.ids.password.disabled = True
        self.ids.confirm_password.disabled = True
        self.ids.dropdown_item.disabled = True
        self.ids.register.disabled = True
        # menu_items 
        menu_items = [
            {
                "text": "CSE",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="CSE": self.menu_callback(x),
            },
            {
                "text": "IT",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="IT": self.menu_callback(x),
            },
            {
                "text": "ENTC",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="ENTC": self.menu_callback(x),
            },
            {
                "text": "Civil",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Civil": self.menu_callback(x),
            },
            {
                "text": "Mech",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Mech": self.menu_callback(x),
            },
            {
                "text": "ELN",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="ELN": self.menu_callback(x),
            },
        ]
        # for dropdown menu
        self.menu = MDDropdownMenu(
            caller = self.ids.dropdown_item,
            items=menu_items,
            width_mult=4,
            max_height = 300
        )
        # self.menu.bind(on_release=self.set_item)
    def verify(self):
        # checking all constraint and adding to database
        nam=self.ids.name.text
        email=self.ids.email.text
        pwdconf=self.ids.confirm_password.text
        pwd=self.ids.password.text
        branch=self.ids.dropdown_item.text
        
        if (len(nam  )==0 or len(nam)>60): # name length
            show_alert_dialog(self,"Enter name in range 1-60!!!")
            return
        if len(nam.split())>0: # name type
            l=nam.split()
            for i in l:
                if re.match(r"([a-zA-Z.]+)",i):
                    continue
                else:
                    show_alert_dialog(self,"Please enter valid name!!!")
                    return
        
        
        if len(email)<1 or len(email)>60: # email lenght
            show_alert_dialog(self,"Please enter an email")
            return 
        
        if  not re.match(r"([a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",email): # email validation
            show_alert_dialog(self,"Please enter valid email!!")
            return
        if len(pwd)==0: # password length
            show_alert_dialog(self,"Please enter a password!!!")
            return
        if len(pwdconf)==0: # confirm password
            show_alert_dialog(self,"Please confirm your password!!!")
            return
        if  (pwdconf != pwd):#match password
            show_alert_dialog(self,"Password do not match!!!")
            return
        
        if (self.ids.dropdown_item.text=="Choose Department"):#check dpartment
            show_alert_dialog(self,"Please Select Department")
            return
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        qur='select name,email from officer'
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        my_cursor.execute(qur)
        for i in my_cursor:
            if email==i[1]:
                show_alert_dialog(self,f"User already registered with username {i[0]}. Please return to Login page!!!")
                return

        # matching dept name with db number
        for k,v in flags.branch.items():
            if v==branch:
                branch=k
                break
        # connecting to database
        query="insert into officer (name,email,password,branch) values (%s , %s ,%s,%s);"
        # hashing password
        hashed = bcrypt.hashpw(pwd.encode('ascii'), bcrypt.gensalt())
        values=(nam,email,hashed.decode('ascii'),branch)
        my_cursor.execute(query,values)
        my_db.commit()
        show_alert_dialog(self,'successfully registered !')
        # setting navbar values
        Login.name_setter(self,nam,flags.branch[branch])
        # changing screen
        self.manager.current = 'home_page'
        self.manager.stack.append(self.name)

    def menu_callback(self, text_item):
        # dropdown menu items
        self.ids.dropdown_item.text = text_item
        self.menu.dismiss()


    def change_field(self,kivy_id):
        # changes focus to next text on pressing enter
        self.ids[kivy_id].focus=True
 
    #sending mail to verify
    def send_mail(self):
        self.officer_email = self.ids.email.text
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        my_cursor.execute(f"select id from officer where email ='{self.officer_email}';")
        records = my_cursor.fetchall()
        if records:
            show_alert_dialog(self,'Already registered with this email')

        else:
            msg = EmailMessage()
            msg['from'] = config("email")
            msg['to'] = self.officer_email
            msg['subject'] = "WIT TNP"
            self.otp=""
            for _ in range(6):
                self.otp+=str(r.randint(1,9))
            msg.set_content(f"Your OTP to register is {self.otp}. Please use it before switching to another page")
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
                    server.login(config("email"),config("email_password"))
                    server.send_message(msg)
                    show_alert_dialog(self,'OTP sent to mail id')
            except Exception:
                show_alert_dialog(self,'Couldnt send OTP due to an error')

    def email_verify(self):
        if self.ids.otp.text == self.otp:
            self.ids.password.disabled = False
            self.ids.password.line_color_normal = flags.app.theme_cls.primary_color
            self.ids.confirm_password.disabled = False
            self.ids.confirm_password.line_color_normal = flags.app.theme_cls.primary_color
            self.ids.register.disabled = False
            self.ids.dropdown_item.disabled = False
            show_alert_dialog(self,'Your email has been verified')
        else:
            show_alert_dialog(self,'Incorrect OTP')