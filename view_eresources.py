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

class EResourceDialog(BoxLayout):
    def __init__(self,**kw):
        super(EResourceDialog, self).__init__(**kw)
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

class ViewEresources(Screen):
    dialog = None
    def __init__(self, **kw):
        super(ViewEresources, self).__init__(**kw)
    
    def full_details(self,id):
        # shows all details of e_resource in a dialog box
        # get self.records from home_screen
        self.id = int(id)
        self.records = self.manager.get_screen('home_page').eresources_records[self.id]
        # create insatance of dialog box,  fill in data and disable everything
        self.dialog_data = EResourceDialog()
        self.dialog_data.ids.dialog_passyear.text = self.records[2]
        self.dialog_data.ids.dialog_branch.text = flags.branch[self.records[3]]
        self.dialog_data.ids.dialog_organizer.text = self.records[4]
        self.dialog_data.ids.dialog_link.text = self.records[5]
        self.dialog_date,self.dialog_time = str(self.records[6]).split(' ')
        self.dialog_data.ids.dialog_visible_date.text = self.dialog_date
        self.dialog_data.ids.dialog_visible_time.text = str(self.records[6]).split(' ')[1]
        self.dialog_data.ids.dialog_description.text = self.records[7]
        self.all_id = ['dialog_passyear','dialog_branch','dialog_organizer','dialog_link','dialog_visible_date','dialog_visible_time','dialog_description']
        # disabling data
        disable_toggler(self.dialog_data,self.all_id,True)

        # create dialog box
        self.dialog = MDDialog(
            title=self.records[1],
            type="custom",
            content_cls=self.dialog_data,
            buttons=[
                    MDRoundFlatButton(text="CANCEL",on_press=self.dismiss_dialog),
                    MDRoundFlatButton(text="SAVE",on_press=self.save_dialog),
                ]
        )
        self.dialog.open()

    def save_dialog(self,instance):
        if not self.dialog_data.ids.dialog_passyear.disabled:
            self.passyear = self.dialog_data.ids.dialog_passyear.text
            self.organizer = self.dialog_data.ids.dialog_organizer.text
            if len(self.organizer)==0 or len(self.organizer) > 60:
                show_alert_dialog(self.dialog_data,"enter name in length range 1 to 60")
                return
            self.link = self.dialog_data.ids.dialog_link.text
            if len(self.organizer)==0:
                show_alert_dialog(self.dialog_data,"enter link")
                return
            self.date = self.dialog_data.ids.dialog_visible_date.text
            self.time = self.dialog_data.ids.dialog_visible_time.text
            date_time = self.date+" "+self.time
            self.visible = datetime.strptime(date_time,'%Y-%m-%d %H:%M:%S')
            self.description=self.dialog_data.ids.dialog_description.text
            my_db, my_cursor = db_connector()
            query = f"UPDATE e_resources SET pass_year = %s, organizer = %s, link = %s,visible = %s, description = %s WHERE id = {self.records[0]}"
            values = (self.passyear, self.organizer, self.link, self.visible, self.description)
            my_cursor.execute(query,values)
            my_db.commit()
            self.dismiss_dialog(self.dialog)
            show_alert_dialog(self,"Modified E-Resources")
            self.manager.callback()
        else:
            self.dismiss_dialog(self.dialog)


    def dismiss_dialog(self,instance):
        # dismiss dialog box
        self.dialog.dismiss()

    def add_delete(self,instance):
        # speeddial button instance
        if instance.icon == 'notebook-plus-outline':
            self.manager.current = 'add_eresources'
            self.manager.stack.append(self.name)

    def edit_eresource(self):
        abc = self.all_id
        del abc[1]
        disable_toggler(self.dialog_data,abc,False)

    def show_date_picker(self):
        # picks date
        year,month,day=self.dialog_date.split('-')
        date_dialog = MDDatePicker(year=int(year),month=int(month),day=int(day))
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self,instance,value,range):
        # saves date value on button text
        self.dialog_data.ids.dialog_visible_date.text = str(value)

    def on_cancel(self,*args):
        # pass on pressing cancel for date picker
        pass

    def show_time_picker(self):
        # picks time
        previous_time = datetime.strptime(self.dialog_time, '%H:%M:%S').time()
        time_dialog = MDTimePicker()
        time_dialog.set_time(previous_time)
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self,args,value):
        # sets time value as button text
        self.dialog_data.ids.dialog_visible_time.text = str(value)
