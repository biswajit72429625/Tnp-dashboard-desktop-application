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

class AssessmentTitle(MDLabel):
    text = StringProperty()
    id = StringProperty()

class AssessmentLabel(MDLabel):
    text = StringProperty()
    id = StringProperty()

class AssessmentCheckbox(MDCheckbox):
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
        view_eresources_screen.ids.grid.clear_widgets()
        # adding dynamic data to screen
        for i in range(len(self.eresources_records)):
            # checkbox, title, date, branch
            view_eresources_screen.ids.grid.add_widget(EResourceCheckbox(id=f'{i}'))
            view_eresources_screen.ids.grid.add_widget(EResourceTitle(id=f'{i}',text=f"[u][ref=world]{self.eresources_records[i][1]}[/ref][/u]"))
            view_eresources_screen.ids.grid.add_widget(EResourceLabel(id=f'{i}',text=f"{str(self.eresources_records[i][6])}"))
            view_eresources_screen.ids.grid.add_widget(EResourceLabel(id=f'{i}',text=f"{self.eresources_records[i][2]}"))
        # query = "insert into e_resources (title,pass_year,branch,organizer,link,description) values (%s,%s,%s,%s,%s,%s);"
        # values = ("apti","2022",6,"apttech","https://www.google.co.in/","very useful")
        # my_cursor.execute(query,values)
        # my_db.commit()

    def load_assessment(self):
        # loads assessments screen
        my_db, my_cursor = db_connector()
        branch = flags.app.officer_branch
        for key, value in flags.branch.items():
            if branch == value:
                branch =key
                break
        query = f"select * from assessment where branch = {branch};"
        my_cursor.execute(query)
        self.assessments_records = my_cursor.fetchall()
        # creating reference for view_assessments screen to put dynamic data in table
        view_assessments_screen = self.manager.get_screen('view_assessments')
        view_assessments_screen.ids.grid.clear_widgets()
        # adding dynamic data to screen
        for i in range(len(self.assessments_records)):
            view_assessments_screen.ids.grid.add_widget(AssessmentCheckbox(id=f'{i}'))
            view_assessments_screen.ids.grid.add_widget(AssessmentTitle(id=f'{i}',text=f"[u][ref=world]{self.assessments_records[i][1]}[/ref][/u]"))
            view_assessments_screen.ids.grid.add_widget(AssessmentLabel(id=f'{i}',text=f"{str(self.assessments_records[i][7])}"))
            view_assessments_screen.ids.grid.add_widget(AssessmentLabel(id=f'{i}',text=f"{self.assessments_records[i][2]}"))
            print(self.assessments_records[i])