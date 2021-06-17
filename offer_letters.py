from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.dialog import MDDialog

class OfferDialog(BoxLayout):
    pass

class OfferLetters(Screen):
    dialog = None
    def __init__(self, **kw):
        super(OfferLetters, self).__init__(**kw)
    
    def full_details(self,row_id):
        # shows all details of e_resource in a dialog box
        self.dialog = MDDialog(
            title=str(self.ids[f'{str(row_id)}'].text),
            type="custom",
            content_cls=OfferDialog(),
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
            self.manager.current = 'add_companies'
            self.manager.stack.append(self.name)
        else:
            pass