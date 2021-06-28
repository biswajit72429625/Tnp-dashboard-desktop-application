from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from datetime import  date
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton
from database import disable_toggler, show_alert_dialog
from kivymd.uix.dialog import MDDialog
import flags
from functools import partial
from mysql.connector.errors import InterfaceError


class AnnouncementDialog(BoxLayout):
    def __init__(self,**kw):
        super(AnnouncementDialog, self).__init__(**kw)
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

class  ViewAnnouncement(Screen):
    def __init__(self, **kw):
        super(ViewAnnouncement, self).__init__(**kw)
    def full_details(self,id):
         # shows all details of Announcement in a dialog box
        self.id = int(id)
        # get self.records from home_screen
        self.records = self.manager.get_screen('home_page').announcement_records[self.id]
        # create insatance of dialog box,  fill in data and disable everything
        self.dialog_data = AnnouncementDialog()
        self.dialog_data.ids.title.text = self.records[1]
        self.dialog_data.ids.description.text = self.records[2]
        self.dialog_data.ids.dialog_passyear.text = self.records[3]
        self.all_id = ['title','description','dialog_passyear']
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
    # if widgets are not disabled, modify the database
        if not self.dialog_data.ids.dialog_passyear.disabled:
            self.passyear = self.dialog_data.ids.dialog_passyear.text
            self.titlee=self.dialog_data.ids.title.text
            self.descriptionn=self.dialog_data.ids.description.text
            if len(self.titlee)==0:
                    show_alert_dialog(self.dialog_data,"enter title")
                    return
            if len(self.descriptionn)==0:
                    show_alert_dialog(self.dialog_data,"enter description")
                    return
            # connecting to database
            my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
            query = f"UPDATE announcement SET pass_year = %s, title = %s, description = %s WHERE id = {self.records[0]}"
            values = (self.passyear, self.titlee, self.descriptionn)
            # pinging database to check for network connection
            try:
                my_db.ping(reconnect=True,attempts=1)
            except InterfaceError:
                show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
                return
            my_cursor.execute(query,values)
            my_db.commit()
            # closing dialog
            self.dismiss_dialog(self.dialog)
            # showing message as modified successfully
            show_alert_dialog(self,"Modified announcement")
            # going to home_screen
            self.manager.callback()
        else:
            # else close dialog
            self.dismiss_dialog(self.dialog)
        
    def dismiss_dialog(self,instance):
        # dismiss dialog box
        self.dialog.dismiss()

    def add_delete(self,instance):
        # speeddial button instance
        if instance.icon == 'notebook-plus-outline':
            self.manager.current = 'add_announcement'
            self.manager.stack.append(self.name)
        else:
            self.delete_announcement()
    def edit_announcement(self):
        # enable all data 
        abc = self.all_id
        #del abc[1]
        disable_toggler(self.dialog_data,abc,False)
        for i in abc:
            self.dialog_data.ids[i].line_color_normal = flags.app.theme_cls.primary_color
    
    def delete_announcement(self):
        # asks if confirm delete?
        checks = self.manager.get_screen('home_page').checkbox_list # list of checkboxes checked
        records = self.manager.get_screen('home_page').announcement_records # list of all records
        self.delete_dialog = MDDialog(
        text="Sure Delete?",
        buttons=[
            MDRoundFlatButton(text="CANCEL",on_press=self.dismiss_delete_dialog),
            MDRoundFlatButton(text="SURE",on_press=partial(self.confirm_delete_dialog,checks,records)),
        ],
        )
        self.delete_dialog.open()

    def dismiss_delete_dialog(self,instance):
        # dismiss delete dialog box
        self.delete_dialog.dismiss()

    def confirm_delete_dialog(self,checks,records,instance):
        # confirm delete from database
        self.dismiss_delete_dialog(self.delete_dialog)
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        # pinging database to check for network connection
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        for i in checks: 
            if i.active:
                my_cursor.execute(f'DELETE FROM announcement WHERE id={records[int(i.id)][0]};')
        my_db.commit()
        show_alert_dialog(self,"announcement deleted")
        # changing screen
        self.manager.callback()