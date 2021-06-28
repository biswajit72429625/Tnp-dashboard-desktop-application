from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from database import show_alert_dialog, send_mail
from datetime import  date
import flags
from mysql.connector.errors import InterfaceError
class AddAnnouncement(Screen):
    def __init__(self, **kw):
        super(AddAnnouncement, self).__init__(**kw)
        today = date.today()
        # dropdown menu for year
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

    def change_field(self,kivy_id):
        # changes focus to next text on pressing enter
        self.ids[kivy_id].focus=True

    def clear(self):
        #to clear all fields
        self.ids.title.text=''
        self.ids.description.text=''
        self.ids.dialog_passyear.text='Passing Year'

    def submit(self):
        # check all constraints and add to database
        self.passs = self.ids.dialog_passyear.text
        self.titlee = self.ids.title.text
        self.descriptionn = self.ids.description.text
        #to check the constraints
        if len(self.titlee) == 0:
            show_alert_dialog(self,"Enter Title")
            return
        if len(self.descriptionn) == 0:
            show_alert_dialog(self,"Enter Description")
            return
        if self.passs == "Passing Year":
            show_alert_dialog(self,"Select Year")
            return
        #connecting to database
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        qur='insert into announcement (title , description ,pass_year, branch ) values (%s,%s,%s,%s)'
        val = (self.titlee,self.descriptionn,self.passs,branch)
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        my_cursor.execute(qur,val)
        my_db.commit()
        send_mail(self,"New Announcement!",f"Title:- {self.titlee}\nDescription:- {self.descriptionn}\nCheck portal for more details",self.passs)
        show_alert_dialog(self,"Announcement added  Sucessfully !!!")
        # clear form
        self.clear()
        # change screen
        self.manager.callback()
        self.manager.callback()