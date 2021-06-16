from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.dialog import MDDialog

class Content(BoxLayout):
    pass

class ManageStudents(Screen):
    def __init__(self, **kw):
        super(ManageStudents, self).__init__(**kw)
    
    def student_details(self,row_id):
        self.dialog = MDDialog(
            type="custom",
            title = self.ids[f'{str(row_id)}'].text,
            content_cls=Content(),
            buttons=[
                    MDRoundFlatButton(text="CANCEL",on_press= self.dismiss_dialog),
                    MDRoundFlatButton(text="SAVE"),
                ])
        self.dialog.open()

    def dismiss_dialog(self,instance):
        self.dialog.dismiss()