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


class HomePage(Screen):
    def __init__(self, **kw):
        super(HomePage, self).__init__(**kw)

    def load_eresource(self):
        my_db, my_cursor = db_connector()
        branch = flags.app.officer_branch
        for key, value in flags.branch.items():
            if branch == value:
                branch = key
                break
        query = f"select title,visible,pass_year from e_resources where branch = '{branch}';"
        my_cursor.execute(query)
        # flags.view_eresources_screen = flags.view_eresources_screen
        flags.view_eresources_screen.ids.grid.add_widget(EResourceCheckbox(id='123'))
        flags.view_eresources_screen.ids.grid.add_widget(EResourceTitle(id='123',text="[u][ref=world]123[/ref][/u]"))
        flags.view_eresources_screen.ids.grid.add_widget(EResourceLabel(id='123',text="label"))
        flags.view_eresources_screen.ids.grid.add_widget(EResourceLabel(id='123',text="label"))
        # query = "insert into e_resources (title,pass_year,branch,organizer,link,description) values (%s,%s,%s,%s,%s,%s);"
        # values = ("apti","2022",6,"apttech","https://www.google.co.in/","very useful")
        # my_cursor.execute(query,values)
        # my_db.commit()

