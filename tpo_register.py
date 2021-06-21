from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from database import db_connector, show_alert_dialog
from login import Login
import flags
import bcrypt
import re

class TpoRegister(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
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
            show_alert_dialog(self,"Please enter a pass!!!")
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
        my_db, my_cursor = db_connector()
        qur='select name,email from officer'
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
        # setting navbar values
        Login.name_setter(self,nam,flags.branch[branch])
        # changing screen
        self.manager.current = 'home_page'
        self.manager.stack.append(self.name)

    def menu_callback(self, text_item):
        # dropdown menu items
        self.ids.dropdown_item.text = text_item
        self.menu.dismiss()


