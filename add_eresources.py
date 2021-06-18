from kivy.uix.screenmanager import Screen
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.menu import MDDropdownMenu
from datetime import date 

class AddEresources(Screen):
    def __init__(self, **kw):
        super(AddEresources,self).__init__(**kw)
        today = date.today()
        menu_items = [
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
            caller = self.ids.dropdown_item,
            items=menu_items,
            width_mult=4,
            max_height = 200
        )

    def menu_callback(self, text_item):
        # sets dropdown wale as text of button and closes dropdown menu
        self.ids.dropdown_item.text = text_item
        self.menu.dismiss()

    def checkbox(self,instance,value):
        if value == True: 
            self.ids.date_label.disabled = True
            self.ids.time_label.disabled = True
        if value == False:
            self.ids.date_label.disabled = False
            self.ids.time_label.disabled = False
        
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
        self.eorganizer=self.ids.e_organizer.text
        self.elink=self.ids.e_link.text
        self.date=self.ids.date_label.text
        self.time=self.ids.time_label.text
        