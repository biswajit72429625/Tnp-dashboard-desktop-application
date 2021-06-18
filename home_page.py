from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.boxlayout import BoxLayout
from database import db_connector
import flags

class EResourceDialog(BoxLayout):
    pass

class EResourceTitle(MDLabel):
    text = StringProperty()
    id = StringProperty()

class EResourceLabel(MDLabel):
    text = StringProperty()
    id = StringProperty()
class EResourceCheckbox(MDCheckbox):
    id = StringProperty()


class HomePage(Screen):
    def __init__(self, **kw):
        super(HomePage, self).__init__(**kw)

    def load_eresource(self):
        # loads e_resources screen
        my_db, my_cursor = db_connector()
        # select branch by officer_branch
        branch = flags.app.officer_branch
        for key, value in flags.branch.items():
            if branch == value:
                branch = key
                break
        # lists all records in database
        query = f"select * from e_resources where branch = '{branch}';"
        my_cursor.execute(query)
        self.eresources_records = my_cursor.fetchall()
        # creating reference for view_eresource screen to put dynamic data in table
        view_eresources_screen = self.manager.get_screen('view_eresources')
        # adding dynamic data to screen
        for i in range(len(self.eresources_records)):
            view_eresources_screen.ids.grid.add_widget(EResourceCheckbox(id=f'{i}'))
            view_eresources_screen.ids.grid.add_widget(EResourceTitle(id=f'{i}',text=f"[u][ref=world]{self.eresources_records[i][1]}[/ref][/u]"))
            view_eresources_screen.ids.grid.add_widget(EResourceLabel(id=f'{i}',text=f"{str(self.eresources_records[i][6])}"))
            view_eresources_screen.ids.grid.add_widget(EResourceLabel(id=f'{i}',text=f"{self.eresources_records[i][2]}"))
        # query = "insert into e_resources (title,pass_year,branch,organizer,link,description) values (%s,%s,%s,%s,%s,%s);"
        # values = ("apti","2022",6,"apttech","https://www.google.co.in/","very useful")
        # my_cursor.execute(query,values)
        # my_db.commit()

