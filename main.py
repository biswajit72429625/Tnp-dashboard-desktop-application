########## kivy modules #########################
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('kivy','window_icon','favicon.ico')
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
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
from view_assessments import ViewAssessments
from add_assessments import AddAssessments
from view_companies import ViewCompanies
from add_companies import AddCompanies
from offer_letters import OfferLetters
from finalize_offer import FinalizeOffer
from analysis import Analysis
from forgot_pass import ForgotPass
from individual_level import IndividualLevel
from department_analysis import DepartmentAnalysis, DepartmentGraphs, DepartmentBasicDetails
from institute_analysis import InstituteAnalysis, InstituteGraphs
from pre_register import PreRegister
from view_announcement import ViewAnnouncement
from add_announcement import AddAnnouncement
#################################################

########## other packages ##################
from os import listdir
import flags
from database import db_connector
################################################

class Manager(ScreenManager):
    stack = []
    def __init__(self, *args):
        super(Manager, self).__init__(*args)
        self.my_db, self.my_cursor = db_connector()
        self.transition = CardTransition()
        # add all screens from here
        self.add_widget(Login(name='login'))
        self.add_widget(ViewEresources(name='view_eresources'))
        self.add_widget(TpoRegister(name='tpo_register'))
        self.add_widget(HomePage(name='home_page'))
        self.add_widget(ManageStudents(name='manage_students'))
        self.add_widget(AddEresources(name='add_eresources'))
        self.add_widget(Placements(name='placements'))
        self.add_widget(ViewAssessments(name='view_assessments'))
        self.add_widget(ViewCompanies(name='view_companies'))
        self.add_widget(AddAssessments(name='add_assessments'))
        self.add_widget(AddCompanies(name='add_companies'))
        self.add_widget(OfferLetters(name='offer_letters'))
        self.add_widget(FinalizeOffer(name='finalize_offer'))
        self.add_widget(Analysis(name='analysis'))
        self.add_widget(ForgotPass(name='forgot_pass'))
        self.add_widget(IndividualLevel(name='individual_level'))
        self.add_widget(DepartmentBasicDetails(name='department_basic_details'))
        self.add_widget(DepartmentAnalysis(name='department_analysis'))
        self.add_widget(DepartmentGraphs(name='department_graphs'))
        self.add_widget(InstituteAnalysis(name='institute_analysis'))
        self.add_widget(InstituteGraphs(name='institute_graphs'))
        self.add_widget(PreRegister(name='pre_register'))
        self.add_widget(ViewAnnouncement(name='view_announcement'))
        self.add_widget(AddAnnouncement(name='add_announcement'))
    
    def callback(self):
        # stack for back button
        if self.stack:
            screen = self.stack.pop()
            self.current = screen


class TnpApp(MDApp):
    # bulding app
    officer_name = StringProperty()
    officer_branch = StringProperty()
    def build(self):
        flags.app=self
        # set theme
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.primary_hue = '600'
        self.theme_cls.accent_palette = 'DeepPurple'
        self.theme_cls.accent_hue = 'A700'
        kv_path = 'KV/'
        for i in listdir(kv_path):
            Builder.load_file(kv_path+i)
        
        return Manager()

if __name__ == '__main__':
    # begin app
    TnpApp().run()
