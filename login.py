from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from database import show_alert_dialog
from mysql.connector.errors import InterfaceError
import flags
import bcrypt
class Login(Screen):
    def __init__(self, **kw):
        super(Login, self).__init__(**kw)
    
    def name_setter(self, name, branch):
        # setting name and branch in all navbar
        app=MDApp.get_running_app()
        app.officer_name= name
        app.officer_branch = branch
    
    def login_checker(self):
        # retriving email and password
        self.email = self.ids.email.text
        self.password = self.ids.password.text
        # connecting to database
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        my_cursor.execute(f"SELECT name,password,branch from officer where email='{self.email}';")
        try:
            # if email found, continue
            record = my_cursor.fetchall()[0]
        except IndexError:
            # else show error
            show_alert_dialog(self,"User not registered")
            return
        name,hashed,branch = record
        # hashing password and comparing if correct
        correct=bcrypt.checkpw(self.password.encode('ascii'),hashed.encode('ascii'))
        if correct:
            # if password is correct, set navbar values and go to home_page
            branch = flags.branch[branch]
            self.name_setter(name,branch)
            self.manager.current = 'home_page'
            self.manager.stack.append(self.name)
        else:
            # else show message
            show_alert_dialog(self,"Invalid password")

        # query = "insert into e_resources (title,pass_year,branch,organizer,link,description) values (%s,%s,%s,%s,%s,%s);"
        # values = ("apti","2022",6,"apttech","https://www.google.co.in/","very useful")
        # my_cursor.execute(query,values)
    def change_field(self,kivy_id):
        # changes focus to next text on pressing enter
        self.ids[kivy_id].focus=True