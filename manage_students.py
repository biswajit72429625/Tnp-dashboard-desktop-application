from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
from database import db_connector, disable_toggler, show_alert_dialog
from datetime import date
import re
import flags

class StudentDialog(BoxLayout):
    def __init__(self, **kw):
        super(StudentDialog, self).__init__(**kw)
        # dropdown menu for pass year
        today = date.today()
        self.yearmenu_items = [
            {   
                "text": str(today.year),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=str(today.year): self.yearmenu_callback(x),
            },
            {
                "text": str(today.year+1),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=str(today.year+1): self.yearmenu_callback(x),
            },
            {
                "text": str(today.year+2),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=str(today.year+2): self.yearmenu_callback(x),
            },
            {
                "text": str(today.year+3),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=str(today.year+3): self.yearmenu_callback(x),
            },
        ]
        self.yearmenu = MDDropdownMenu(
            caller = self.ids.dialog_passyear,
            items=self.yearmenu_items,
            width_mult=4,
            max_height = 200
            )

        # menu_items 
        branchmenu_items = [
            {
                "text": "CSE",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="CSE": self.branchmenu_callback(x),
            },
            {
                "text": "IT",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="IT": self.branchmenu_callback(x),
            },
            {
                "text": "ENTC",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="ENTC": self.branchmenu_callback(x),
            },
            {
                "text": "Civil",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Civil": self.branchmenu_callback(x),
            },
            {
                "text": "Mech",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Mech": self.branchmenu_callback(x),
            },
            {
                "text": "ELN",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="ELN": self.branchmenu_callback(x),
            },
        ]
        # for dropdown menu
        self.branchmenu = MDDropdownMenu(
            caller = self.ids.dialog_branch,
            items=branchmenu_items,
            width_mult=4,
            max_height = 300
        )

    def yearmenu_callback(self, text_item):
        # callback menu for pass year
        self.ids.dialog_passyear.text = text_item
        self.yearmenu.dismiss()

    def branchmenu_callback(self, text_item):
        # callback menu for branch
        self.ids.dialog_branch.text = text_item
        self.branchmenu.dismiss()


class StudentTitle(MDLabel):
    text = StringProperty()
    id = StringProperty()

class StudentLabel(MDLabel):
    text = StringProperty()
    id = StringProperty()

class ManageStudents(Screen):
    def __init__(self, **kw):
        super(ManageStudents, self).__init__(**kw)
    
    def load_students(self,year):
        # loads students screen

        # changing color of button pressed
        for i in range(4):
            if i == year:
                self.ids[str(year)].md_bg_color = flags.app.theme_cls.primary_color
            else:
                self.ids[str(i)].md_bg_color = flags.app.theme_cls.accent_color
        my_db, my_cursor = db_connector()
        # select branch by officer_branch
        branch = flags.app.officer_branch
        for key, value in flags.branch.items():
            if branch == value:
                branch = key
                break
        # lists all records in database
        query = f"select * from students where branch = '{branch}' and pass_year = {date.today().year+year};"
        my_cursor.execute(query)
        self.student_records = my_cursor.fetchall()
        # adding dynamic data to screen
        self.ids.grid.clear_widgets()
        for i in range(len(self.student_records)):
            # enrollmentid, name, email
            self.ids.grid.add_widget(StudentTitle(id=f'{i}',text=f"[u][ref=world]{self.student_records[i][0]}[/ref][/u]"))
            self.ids.grid.add_widget(StudentLabel(id=f'{i}',text=f"{str(self.student_records[i][1])}"))
            self.ids.grid.add_widget(StudentLabel(id=f'{i}',text=f"{self.student_records[i][3]}"))

    def full_details(self,id):
        # shows all details of e_resource in a dialog box
        self.id = int(id)# create insatance of dialog box,  fill in data and disable everything
        self.dialog_data = StudentDialog()
        self.dialog_data.ids.dialog_name.text = self.student_records[self.id][1]
        self.dialog_data.ids.dialog_phone.text = self.student_records[self.id][2]
        self.dialog_data.ids.dialog_email.text = self.student_records[self.id][3]
        self.dialog_data.ids.dialog_passyear.text = self.student_records[self.id][5]
        self.dialog_data.ids.dialog_branch.text = flags.branch[self.student_records[self.id][6]]
        self.all_id = ['dialog_name','dialog_phone','dialog_email','dialog_passyear','dialog_branch']
        # disabling data
        disable_toggler(self.dialog_data,self.all_id,True)
        # shows all details of e_resource in a dialog box
        self.dialog = MDDialog(
            title=str(self.student_records[self.id][0]),
            type="custom",
            content_cls=self.dialog_data,
            buttons=[
                    MDRoundFlatButton(text="CANCEL",on_press=self.dismiss_dialog),
                    MDRoundFlatButton(text="SAVE", on_press= self.save_dialog_again),
                ]
        )
        self.dialog.open()

    def dismiss_dialog(self,instance):
        self.dialog.dismiss()

    def edit_student(self):
        # enables all input fields to edit students
        disable_toggler(self.dialog_data,self.all_id,False)

    def save_dialog(self,instance):
        # if widgets are not disabled, modify the database
        if not self.dialog_data.ids.dialog_name.disabled:
            self.name = self.dialog_data.ids.dialog_name.text
            # checking name constraint
            if len(self.name)==0 or len(self.name) > 60:
                show_alert_dialog(self.dialog_data,"enter name in length range 1 to 60")
                return
            self.phone = self.dialog_data.ids.dialog_phone.text
            # checking phone number constraint
            if len(self.phone) != 10:
                show_alert_dialog(self.dialog_data,"enter 10 digit phone number")
                return
            try:
                phone = int(self.phone)
            except ValueError:
                show_alert_dialog(self.dialog_data,"enter valid phone number")
                return
            self.email = self.dialog_data.ids.dialog_email.text
            # checking email constraint
            if len(self.email)<1 or len(self.email)>60: # email length
                show_alert_dialog(self,"Please enter an email")
                return 
            if  not re.match(r"([a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",self.email): # email validation
                show_alert_dialog(self,"Please enter valid email!!")
                return
            self.passyear = self.dialog_data.ids.dialog_passyear.text
            self.branch = self.dialog_data.ids.dialog_branch.text
            # matching dept name with db number
            for k,v in flags.branch.items():
                if v==self.branch:
                    self.branch=k
                    break
            # connecting to database
            my_db, my_cursor = db_connector()
            query = f"UPDATE students SET stud_name = %s, stud_phone_no = %s, stud_email = %s,pass_year = %s, branch = %s WHERE enrollment_id = {self.student_records[self.id][0]}"
            print(self.name,self.phone, self.email, self.passyear, self.branch, self.student_records[self.id][0])
            values = (self.name,self.phone, self.email, self.passyear, self.branch)
            my_cursor.execute(query,values)
            my_db.commit()
            # closing dialog
            self.dismiss_dialog(self.dialog)
            # showing message as modified successfully
            show_alert_dialog(self,"Modified Student")
            # going to home_screen
            self.manager.callback()
        else:
            # else close dialog
            self.dismiss_dialog(self.dialog)

    def save_dialog_again(self,instance):
        if not self.dialog_data.ids.dialog_name.disabled:
            self.name = self.dialog_data.ids.dialog_name.text
            self.phone = self.dialog_data.ids.dialog_phone.text
            self.email = self.dialog_data.ids.dialog_email.text
            self.passyear = self.dialog_data.ids.dialog_passyear.text
            self.branch = self.dialog_data.ids.dialog_branch.text
            for k,v in flags.branch.items():
                if v==self.branch:
                    self.branch = k
                    break
            my_db, my_cursor = db_connector()
            query = f"UPDATE students SET stud_name = %s, stud_phone_no = %s, stud_email = %s, pass_year = %s, branch = %s where enrollment_id = %s;"
            values = (self.name, self.phone, self.email, self.passyear, self.branch, self.student_records[self.id][0])
            my_cursor.execute(query,values)
            my_db.commit()
            self.dismiss_dialog(self.dialog)
            show_alert_dialog(self,"Student modified successfully!")
            self.manager.callback()
        else:
            self.dismiss_dialog(self.dialog)