from kivy.uix.screenmanager import Screen
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.menu import MDDropdownMenu
from database import show_alert_dialog
from datetime import datetime


class AddEresources(Screen):
    def __init__(self, **kw):
        super(AddEresources,self).__init__(**kw)
        menu_items = [
            {
                "text": "CSE",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="CSE": self.menu_callback(x),
            },
            {
                "text": "IT",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="IT": self.menu_callback(x),
            },
            {
                "text": "ENTC",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="ENTC": self.menu_callback(x),
            },
            {
                "text": "Civil",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Civil": self.menu_callback(x),
            },
            {
                "text": "Mech",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Mech": self.menu_callback(x),
            },
            {
                "text": "ELN",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="ELN": self.menu_callback(x),
            },
        ]
        self.menu = MDDropdownMenu(
            caller = self.ids.dropdown_item,
            items=menu_items,
            width_mult=4,
            max_height = 300
        )

    def menu_callback(self, text_item):
        # sets dropdown wale as text of button and closes dropdown menu
        self.ids.dropdown_item.text = text_item
        self.menu.dismiss()

    def checkbox(self,instance,value):
        if value == True:
            current_time = datetime.now() 
            self.ids.date_label.disabled = True
            self.ids.time_label.disabled = True
            self.ids.date_label.text = str(" "+str(current_time.day)+"-"+str(current_time.month)+"-"+str(current_time.year)+" ")
            self.ids.time_label.text = str(" "+" "+" "+str(current_time.hour)+" "+" : "+" "+str(current_time.minute)+" "+"  "+" "+" ")
        if value == False:
            self.ids.date_label.disabled = False
            self.ids.time_label.disabled = False
            self.ids.date_label.text = "Select Date"
            self.ids.time_label.text = "Select Time"
    def show_date_picker(self):
        # picks date
        date_dialog = MDDatePicker(year=2021,month=2,day=14)
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self,instance,value,range):
        # saves date value on button text
        self.ids.date_label.text = str(value)

    def on_cancel(self,*args):
        # pass on pressing cancel for date picker
        pass

    def show_time_picker(self):
        # picks time
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self,args,value):
        # sets time value as button text
        self.ids.time_label.text = str(value)

    def submit(self):
        self.ename=self.ids.e_name.text
        self.eorganizer=self.ids.e_organiser.text
        self.elink=self.ids.e_link.text
        date=self.ids.date_label.text
        time=self.ids.time_label.text
        date_time = date+" "+time
        self.date = datetime.strptime(date_time,'%Y-%m-%d %H:%M:%S')
        if len(self.name) > 20:
            show_alert_dialog(self,"Title should be less than 20 characters")
        elif len(self.eorganizer) > 60:
            show_alert_dialog(self,"Organiser should be less than 60 characters")
        
        