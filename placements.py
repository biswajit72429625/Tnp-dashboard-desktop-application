from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from database import db_connector
import flags

class EResourceTitle(MDLabel):
    text = StringProperty()
    id = StringProperty()

class EResourceLabel(MDLabel):
    text = StringProperty()
    id = StringProperty()

class EResourceCheckbox(MDCheckbox):
    id = StringProperty()

class Placements(Screen):
    def __init__(self, **kw):
        super(Placements, self).__init__(**kw)
    
    def load_companies(self):
        # loads e_resources screen
        my_db, my_cursor = db_connector()
        # select branch by officer_branch
        branch = flags.app.officer_branch
        for key, value in flags.branch.items():
            if branch == value:
                branch = key
                break
        # lists all records in database
        query = f"select * from company where branch = '{branch}';"
        my_cursor.execute(query)
        self.company_records = my_cursor.fetchall()
        # creating reference for view_eresource screen to put dynamic data in table
        view_companies_screen = self.manager.get_screen('view_companies')
        view_companies_screen.ids.grid.clear_widgets()
        self.company_checkbox_list = []
        # adding dynamic data to screen
        for i in range(len(self.company_records)):
            # checkbox, title, date, branch
            check = EResourceCheckbox(id=f'{i}')
            self.company_checkbox_list.append(check)
            view_companies_screen.ids.grid.add_widget(check)
            view_companies_screen.ids.grid.add_widget(EResourceTitle(id=f'{i}',text=f"[u][ref=world]{self.company_records[i][1]}[/ref][/u]"))
            view_companies_screen.ids.grid.add_widget(EResourceLabel(id=f'{i}',text=f"{str(self.company_records[i][6])}"))
            view_companies_screen.ids.grid.add_widget(EResourceLabel(id=f'{i}',text=f"{self.company_records[i][2]}"))


