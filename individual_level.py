from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton
from kivy.properties import StringProperty
import flags

class IndividualDialog(BoxLayout):
    pass

class IndividualTitle(MDLabel):
    text = StringProperty()
    id = StringProperty()

class IndividualLabel(MDLabel):
    text = StringProperty()
    id = StringProperty()

class IndividualLevel(Screen):
    def __init__(self, **kw):
        super(IndividualLevel, self).__init__(**kw)

    def load_table(self):
        # loads individual level analysis screen

        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        # select branch by officer_branch
        branch = flags.app.officer_branch
        for key, value in flags.branch.items():
            if branch == value:
                branch = key
                break
        # lists all records in database
        query = f'''
            select st.enrollment_id, st.stud_name, st.stud_email, co.name, co.role, co.package, co.platform, co.website, ol.link, ol.date_of_interview, ol.date_of_offer
            from offer_letters as ol
            inner join students as st on ol.enrollment_id = st.enrollment_id
            inner join company as co on ol.company_id = co.company_id
            where st.pass_year = YEAR(CURDATE()) and st.branch= {branch} and ol.finalised is not NULL;
        '''
        my_cursor.execute(query)
        self.finalised_records = my_cursor.fetchall()
        # adding dynamic data to screen
        self.ids.grid.clear_widgets()
        for i in range(len(self.finalised_records)):
            # enrollmentid, stud_name, company, role, package
            self.ids.grid.add_widget(IndividualTitle(id=f'{i}',text=f"[u][ref=world]{self.finalised_records[i][0]}[/ref][/u]"))
            self.ids.grid.add_widget(IndividualLabel(id=f'{i}',text=f"{str(self.finalised_records[i][1])}"))
            self.ids.grid.add_widget(IndividualLabel(id=f'{i}',text=f"{self.finalised_records[i][3]}"))
            self.ids.grid.add_widget(IndividualLabel(id=f'{i}',text=f"{self.finalised_records[i][4]}"))
            self.ids.grid.add_widget(IndividualLabel(id=f'{i}',text=f"{self.finalised_records[i][5]}"))

    def full_details(self,row_id):
        # shows all details of student in a dialog box
        self.id = int(row_id)
        # create insatance of dialog box,  fill in data and disable everything
        self.dialog_data = IndividualDialog()
        self.dialog_data.ids.dialog_student_name.text = self.finalised_records[self.id][1]
        self.dialog_data.ids.dialog_student_email.text = self.finalised_records[self.id][2]
        self.dialog_data.ids.dialog_company_name.text = self.finalised_records[self.id][3]
        self.dialog_data.ids.dialog_company_role.text = self.finalised_records[self.id][4]
        self.dialog_data.ids.dialog_company_package.text = str(self.finalised_records[self.id][5])
        self.dialog_data.ids.dialog_company_platform.text = "On-Campus" if self.finalised_records[self.id][6] == '' else "Off-Campus"
        # self.dialog_data.ids.dialog_website_link.text = self.finalised_records[self.id][7]
        # self.dialog_data.ids.dialog_offer_link.text = self.finalised_records[self.id][8]
        self.dialog_data.ids.dialog_date_of_interview.text = str(self.finalised_records[self.id][9])
        self.dialog_data.ids.dialog_date_of_offer_letter.text = str(self.finalised_records[self.id][10])
        # shows all details of offer letter in a dialog box
        self.dialog = MDDialog(
            title=str(self.finalised_records[self.id][0]),
            type="custom",
            content_cls=self.dialog_data,
            buttons=[
                    MDRoundFlatButton(text="CANCEL",on_press=self.dismiss_dialog)
                ]
        )
        self.dialog.open()

    def dismiss_dialog(self,instance):
        self.dialog.dismiss()
