from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.menu import MDDropdownMenu
from datetime import datetime, date
from database import db_connector, disable_toggler, show_alert_dialog
import flags

class AssessmentDialog(BoxLayout):
    def __init__(self,**kw):
        super(AssessmentDialog, self).__init__(**kw)
        today = date.today()
        self.menu_items = [
            {   
                "text": str(today.year),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=str(today.year): self.menu_callback(x),
            },
            {
                "text": str(today.year+1),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=str(today.year+1): self.menu_callback(x),
            },
            {
                "text": str(today.year+2),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=str(today.year+2): self.menu_callback(x),
            },
            {
                "text": str(today.year+3),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=str(today.year+3): self.menu_callback(x),
            },
        ]
        self.menu = MDDropdownMenu(
            caller = self.ids.dialog_passyear,
            items=self.menu_items,
            width_mult=4,
            max_height = 200
            )
    def menu_callback(self, text_item):
        # sets dropdown wale as text of button and closes dropdown menu
        self.ids.dialog_passyear.text = text_item
        self.menu.dismiss()

class ViewAssessments(Screen):
    dialog = None
    def __init__(self, **kw):
        super(ViewAssessments, self).__init__(**kw)
    
    def full_details(self,id):
        # shows all details of e_resource in a dialog box
        self.id = int(id)
        # get self.records from home_screen
        self.records = self.manager.get_screen('home_page').assessments_records[self.id]
        # create insatance of dialog box,  fill in data and disable everything
        self.dialog_data = AssessmentDialog()
        self.dialog_data.ids.dialog_passyear.text = self.records[2]
        self.dialog_data.ids.dialog_branch.text = flags.branch[self.records[3]]
        self.dialog_data.ids.dialog_organizer.text = self.records[4]
        self.dialog_data.ids.dialog_link.text = self.records[5]
        if self.records[6] == None:
            self.dialog_data.ids.dialog_resultlink.text = ''
        else:
            self.dialog_data.ids.dialog_resultlink.text = self.records[6]
        self.dialog_date,self.dialog_time = str(self.records[7]).split(' ')
        self.dialog_data.ids.dialog_visible_date.text = self.dialog_date
        self.dialog_data.ids.dialog_visible_time.text = self.dialog_time
        self.all_id = ['dialog_passyear','dialog_branch','dialog_organizer','dialog_link','dialog_resultlink','dialog_visible_date','dialog_visible_time']
        # disabling data
        disable_toggler(self.dialog_data,self.all_id,True)
        # shows all details of e_resource in a dialog box
        self.dialog = MDDialog(
            title=self.records[1],
            type="custom",
            content_cls=AssessmentDialog(),
            buttons=[
                    MDRoundFlatButton(text="CANCEL",on_press=self.dismiss_dialog),
                    MDRoundFlatButton(text="SAVE"),
                ]
        )
        self.dialog.open()

    def dismiss_dialog(self,instance):
        self.dialog.dismiss()

    def add_delete(self,instance):
        if instance.icon == 'notebook-plus-outline':
            self.manager.current = 'add_assessments'
            self.manager.stack.append(self.name)