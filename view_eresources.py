from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivymd.app import MDApp
from kivy.metrics import dp

class ViewEresources(Screen):
    def __init__(self, **kw):
        super(ViewEresources, self).__init__(**kw)
        # self.table = MDDataTable(size_hint= (0.8,0.7),
        # pos_hint= {'center_x':0.425, 'center_y':0.4},
        # column_data= [("Name",dp(40)),("Date",dp(40)),("Year",dp(40))],
        # row_data= [("[size=30]1[/size]","19-11-2000","3rd"),("","","")])
        # self.add_widget(self.table)
