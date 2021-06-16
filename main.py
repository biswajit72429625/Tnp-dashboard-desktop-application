########## kivy modules #########################
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import CardTransition
###################################################

############ screens ############################
from login import Login
from view_eresources import ViewEresources
from tpo_register import TpoRegister
from home_page import HomePage
from manage_students import ManageStudents
from add_eresources import AddEresources
from placements import Placements
#################################################

########## other packages ##################
from os import listdir
import flags
################################################

class Manager(ScreenManager):
    stack = []
    def __init__(self, *args):
        super(Manager, self).__init__(*args)
        self.transition = CardTransition()
        # add all screens from here
        self.add_widget(Login(name='login'))
        self.add_widget(ViewEresources(name='view_eresources'))
        self.add_widget(TpoRegister(name='tpo_register'))
        self.add_widget(HomePage(name='home_page'))
        self.add_widget(ManageStudents(name='manage_students'))
        self.add_widget(AddEresources(name='add_eresources'))
        self.add_widget(Placements(name='placements'))
    
    def callback(self):
        if self.stack:
            screen = self.stack.pop()
            self.current = screen


class TnpApp(MDApp):
    def build(self):
        flags.app=self
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.primary_hue = '600'
        self.theme_cls.accent_palette = 'DeepPurple'
        self.theme_cls.accent_hue = 'A700'
        kv_path = 'KV/'
        for i in listdir(kv_path):
            Builder.load_file(kv_path+i)
        
        return Manager()

if __name__ == '__main__':
    TnpApp().run()
