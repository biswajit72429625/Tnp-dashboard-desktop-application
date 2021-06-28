from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton
from kivy.properties import StringProperty
from openpyxl import Workbook
from database import show_alert_dialog
from mysql.connector.errors import InterfaceError
from datetime import date
import flags
import os

class IndividualDialog(BoxLayout):
    # full details for individual details
    pass

class ExportDialog(BoxLayout):
    # exporting data to excel
    pass

class IndividualTitle(MDLabel):
    # individual title label
    text = StringProperty()
    id = StringProperty()

class IndividualLabel(MDLabel):
    # individual label
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
        # pinging database to check for network connection
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
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
        # closes full details dialog
        self.dialog.dismiss()

    def export(self):
        # confirm export dialog
        self.export_data = ExportDialog()
        self.export_dialog = MDDialog(
            title="Export Columns",
            type="custom",
            content_cls=self.export_data,
            buttons=[
                    MDRoundFlatButton(text="CANCEL",on_press=self.dismiss_export_dialog),
                    MDRoundFlatButton(text="EXPORT",on_press=self.make_excel)
                ]
        )
        self.export_dialog.open()

    def dismiss_export_dialog(self,instance):
        # closes full details dialog
        self.export_dialog.dismiss()

    def make_excel(self, instance):
        # exporting to excel file
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        # select branch by officer_branch
        branch = flags.app.officer_branch
        for key, value in flags.branch.items():
            if branch == value:
                branch = key
                break
        # retrive dynamic column names
        columns = ""
        for i in self.export_data.ids.keys():
            if self.export_data.ids[i].active:
                columns+=i+","
        columns = columns[:-1]
        # execute query
        query = "SELECT "+columns+f'''
            from offer_letters as ol
            inner join students as st on ol.enrollment_id = st.enrollment_id
            inner join company as co on ol.company_id = co.company_id
            where st.pass_year = YEAR(CURDATE()) and st.branch= {branch} and ol.finalised is not NULL;
            '''
        # pinging database to check for network connection
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        my_cursor.execute(query)
        # retrive data
        data=my_cursor.fetchall()
        platform_check = 0
        # excel sheet name
        sheet_title = "Passout "+str(date.today().year)
        # preparing excel sheet
        wb = Workbook()
        wb['Sheet'].title = sheet_title
        sh1 = wb.active
        # setting column name
        header = columns.split(',')
        for i in range(len(header)):
            sh1[chr(ord('A')+i)+'1'].value = header[i][3:]
            # checking if company platorm is to be exported
            if header[i][3:]=='platform':
                platform_check = i
        # entering all rows
        for i in range(len(data)):
            for ii in range(len(header)):
                if platform_check and ii==platform_check:
                    # if platform '' entering on-campus, else off-campus
                    if data[i][ii] == '':
                        sh1[chr(ord('A')+ii)+str(2+i)].value = 'On-Campus'
                    else:
                        sh1[chr(ord('A')+ii)+str(2+i)].value = 'Off-Campus'
                else:
                    sh1[chr(ord('A')+ii)+str(2+i)].value = data[i][ii]
        # resiszing colun width
        for col in sh1.columns:
            max_length = 0
            column = col[0].column_letter # Get the column name
            for cell in col:
                try: # Necessary to avoid error on empty cells
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except Exception:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            sh1.column_dimensions[column].width = adjusted_width
        # making directory if dosent exist
        try:
            os.makedirs(f"C:\\Users\\{os.getlogin()}\\Downloads\\tnp")
        except FileExistsError:
            pass
        # saving excel sheet
        wb.save(f"C:\\Users\\{os.getlogin()}\\Downloads\\tnp\\{sheet_title}.xlsx")
        show_alert_dialog(self,"File saved to Downloads folder")
        self.dismiss_export_dialog(self.export_dialog)
        