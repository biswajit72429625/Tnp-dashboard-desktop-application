from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

class ViewEresources(Screen):
    def __init__(self, **kw):
        super(ViewEresources, self).__init__(**kw)
        self.table = MDDataTable(size_hint= (0.9,0.6),
        elevation = 20,
        pos_hint= {'center_x':0.5, 'center_y':0.5},
        column_data= [("Name",dp(20)),("Date",dp(20)),("Year",dp(20))],
        row_data= [("[size=15]1[/size]","19-11-2000","3rd"),("","","")])
        self.add_widget(self.table)
