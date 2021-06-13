########## inbuilt libraries ##################
from os import listdir
################################################

########## kivy modules #########################
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import CardTransition
###################################################

############ screens ############################
from login import Login
from tpo_register import TpoRegister
from home_page import HomePage
#################################################

class Manager(ScreenManager):
     def __init__(self, *args):
        super(Manager, self).__init__(*args)
        self.transition = CardTransition()
        # add all screens from here
        self.add_widget(Login(name='login'))
        self.add_widget(TpoRegister(name='tpo_register'))
        self.add_widget(HomePage(name='home_page'))


class TnpApp(MDApp):
    def build(self):
        kv_path = 'KV/'
        for i in listdir(kv_path):
            Builder.load_file(kv_path+i)
        return Manager()

if __name__ == '__main__':
    TnpApp().run()
