from kivy.uix.screenmanager import Screen
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.picker import MDTimePicker


class AddEresources(Screen):
    def _init_(self, **kw):
        super(AddEresources, self)._init_(**kw)
    def show_date_picker(self):
        date_dialog = MDDatePicker(year=2021,month=2,day=14)
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    def on_save(self,instance,value,range):
        self.ids.date_label.text = str(value)
    def on_cancel(self,*args):
        pass
    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()
    def get_time(self,args,value):
        self.ids.time_label.text = str(value)

