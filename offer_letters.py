from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty
import flags
from datetime import date
from database import disable_toggler, show_alert_dialog, get_close_matches_indexes

class OfferDialog(BoxLayout):
    pass

class OfferLetterTitle(MDLabel):
    text = StringProperty()
    id = StringProperty()

class OfferLetterLabel(MDLabel):
    text = StringProperty()
    id = StringProperty()

class OfferLetters(Screen):
    dialog = None
    def __init__(self, **kw):
        super(OfferLetters, self).__init__(**kw)
        menu_items = [
            {
                "text": "Student Name",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Student Name": self.menu_callback(x),
            },
            {
                "text": "Company Name",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Company Name": self.menu_callback(x),
            },
            {
                "text": "Role",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Role": self.menu_callback(x),
            },
            {
                "text": "Package",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Package": self.menu_callback(x),
            },
        ]
        self.menu = MDDropdownMenu(
            caller = self.ids.dropdown_item,
            items=menu_items,
            width_mult=4,
            max_height = 150
        )
    
    def full_details(self,row_id):
        # shows all details of student in a dialog box
        self.id = int(row_id)
        # create insatance of dialog box,  fill in data and disable everything
        self.dialog_data = OfferDialog()
        self.dialog_data.ids.dialog_student_name.text = self.offer_records[self.id][1]
        self.dialog_data.ids.dialog_student_email.text = self.offer_records[self.id][2]
        self.dialog_data.ids.dialog_company_name.text = self.offer_records[self.id][3]
        self.dialog_data.ids.dialog_company_role.text = self.offer_records[self.id][4]
        self.dialog_data.ids.dialog_company_package.text = str(self.offer_records[self.id][5])
        self.dialog_data.ids.dialog_company_platform.text = "On-Campus" if self.offer_records[self.id][6] == '' else "Off-Campus"
        self.dialog_data.ids.dialog_offer_link.text = self.offer_records[self.id][7]
        self.dialog_data.ids.dialog_date_of_interview.text = str(self.offer_records[self.id][8])
        self.dialog_data.ids.dialog_date_of_offer_letter.text = str(self.offer_records[self.id][9])
        self.dialog_data.ids.dialog_finalised.text = "Confirmed" if self.offer_records[self.id][10] == '' else "Not-Confirmed"
        self.all_id = ['dialog_student_name','dialog_student_email','dialog_company_name','dialog_company_role','dialog_company_package',
                        'dialog_company_platform','dialog_date_of_interview','dialog_date_of_offer_letter','dialog_finalised']
        # disabling data
        disable_toggler(self.dialog_data,self.all_id,True)
        # shows all details of offer letter in a dialog box
        self.dialog = MDDialog(
            title=str(self.offer_records[self.id][0]),
            type="custom",
            content_cls=self.dialog_data,
            buttons=[
                    MDRoundFlatButton(text="CANCEL",on_press=self.dismiss_dialog),
                    MDRoundFlatButton(text="SAVE", on_press= self.save_dialog),
                ]
        )
        self.dialog.open()

    def dismiss_dialog(self,instance):
        self.dialog.dismiss()

    def menu_callback(self, text_item):
        self.ids.dropdown_item.text = text_item
        self.menu.dismiss()

    def load_offer(self,year):
        # loads students screen

        # changing color of button pressed
        for i in range(2):
            if i == year:
                self.ids[str(year)].md_bg_color = flags.app.theme_cls.primary_color
            else:
                self.ids[str(i)].md_bg_color = flags.app.theme_cls.accent_color
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        # select branch by officer_branch
        branch = flags.app.officer_branch
        for key, value in flags.branch.items():
            if branch == value:
                branch = key
                break
        # lists all records in database
        query = '''
            select st.enrollment_id, st.stud_name, st.stud_email, co.name, co.role, co.package, co.platform, ol.link, ol.date_of_interview, ol.date_of_offer, ol.finalised
            from offer_letters as ol
            inner join students as st on ol.enrollment_id = st.enrollment_id
            inner join company as co on ol.company_id = co.company_id
            where st.pass_year = %s and st.branch=%s;
        '''
        values = (date.today().year+year,branch)
        my_cursor.execute(query,values)
        self.offer_records = my_cursor.fetchall()
        # adding dynamic data to screen
        self.ids.grid.clear_widgets()
        for i in range(len(self.offer_records)):
            # stud_name, company, role
            self.ids.grid.add_widget(OfferLetterTitle(id=f'{i}',text=f"[u][ref=world]{self.offer_records[i][1]}[/ref][/u]"))
            self.ids.grid.add_widget(OfferLetterLabel(id=f'{i}',text=f"{str(self.offer_records[i][3])}"))
            self.ids.grid.add_widget(OfferLetterLabel(id=f'{i}',text=f"{self.offer_records[i][4]}"))

    def edit_offer(self):
        disable_toggler(self.dialog_data,['dialog_finalised'],False)

    def save_dialog(self,instance):
        if not self.dialog_data.ids.dialog_finalised.disabled:
            finalised = '' if self.dialog_data.ids.dialog_finalised.text == "Confirmed" else None
            # my_db, my_cursor = db_connector()
            my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
            query = "update offer_letters set finalised = %s where enrollment_id = %s and company_id = (select company_id from company where name = %s and role = %s);"
            values = (finalised,self.offer_records[self.id][0], self.offer_records[self.id][3], self.offer_records[self.id][4])
            my_cursor.execute(query,values)
            my_db.commit()
            # closing dialog
            self.dismiss_dialog(self.dialog)
            # showing message as modified successfully
            show_alert_dialog(self,"Modified offer letter status")
            # going to home_screen
            self.manager.callback()
        else:
            # else close dialog
            self.dismiss_dialog(self.dialog)

    def search_data(self):
        if self.ids.dropdown_item.text == "Search by":
            show_alert_dialog(self,"Please select a search type")
            return
        if len(self.ids.search_text.text) == 0:
            show_alert_dialog(self,"Please enter text to search with")
            return
        year = 0 if self.ids['0'].md_bg_color == flags.app.theme_cls.primary_color else 1        
        # select branch by officer_branch
        branch = flags.app.officer_branch
        for key, value in flags.branch.items():
            if branch == value:
                branch = key
                break
        # lists all records in database
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        query = '''
            select st.enrollment_id, st.stud_name, st.stud_email, co.name, co.role, co.package, co.platform, ol.link, ol.date_of_interview, ol.date_of_offer, ol.finalised
            from offer_letters as ol
            inner join students as st on ol.enrollment_id = st.enrollment_id
            inner join company as co on ol.company_id = co.company_id
            where st.pass_year = %s and st.branch=%s;
        '''
        values = (date.today().year+year,branch)
        my_cursor.execute(query,values)
        self.offer_records = my_cursor.fetchall()
        if self.ids.dropdown_item.text == 'Student Name':
            best_search = get_close_matches_indexes(self.ids.search_text.text,[i[1] for i in self.offer_records],n=200,cutoff=0.6)
        elif self.ids.dropdown_item.text == 'Company Name':
            best_search = get_close_matches_indexes(self.ids.search_text.text,[i[3] for i in self.offer_records],n=200,cutoff=0.6)
        elif self.ids.dropdown_item.text == 'Role':
            best_search = get_close_matches_indexes(self.ids.search_text.text,[i[4] for i in self.offer_records],n=200,cutoff=0.6)
        else:
            best_search = get_close_matches_indexes(self.ids.search_text.text,[str(i[5]) for i in self.offer_records],n=200,cutoff=0.6)
        self.offer_records = [self.offer_records[i] for i in best_search]
        # adding dynamic data to screen
        self.ids.grid.clear_widgets()
        for i in range(len(self.offer_records)):
            # stud_name, company, role
            self.ids.grid.add_widget(OfferLetterTitle(id=f'{i}',text=f"[u][ref=world]{self.offer_records[i][1]}[/ref][/u]"))
            self.ids.grid.add_widget(OfferLetterLabel(id=f'{i}',text=f"{str(self.offer_records[i][3])}"))
            self.ids.grid.add_widget(OfferLetterLabel(id=f'{i}',text=f"{self.offer_records[i][4]}"))
        
    def sort_by(self,by):
        self.offer_records = sorted(self.offer_records,key=lambda x: x[by])
        # adding dynamic data to screen
        self.ids.grid.clear_widgets()
        for i in range(len(self.offer_records)):
            # stud_name, company, role
            self.ids.grid.add_widget(OfferLetterTitle(id=f'{i}',text=f"[u][ref=world]{self.offer_records[i][1]}[/ref][/u]"))
            self.ids.grid.add_widget(OfferLetterLabel(id=f'{i}',text=f"{str(self.offer_records[i][3])}"))
            self.ids.grid.add_widget(OfferLetterLabel(id=f'{i}',text=f"{self.offer_records[i][4]}"))