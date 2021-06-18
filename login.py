from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
class Login(Screen):
    def __init__(self, **kw):
        super(Login, self).__init__(**kw)
    
    def name_setter(self):
        # setting name and branch in all navbar
        app=MDApp.get_running_app()
        app.officer_name= self.ids.email.text
        app.officer_branch = self.ids.password.text