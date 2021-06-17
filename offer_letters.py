from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

class OfferDialog(BoxLayout):
    pass

class OfferLetters(Screen):
    dialog = None
    def __init__(self, **kw):
        super(OfferLetters, self).__init__(**kw)
        menu_items = [
            {
                "text": "Name",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Name": self.menu_callback(x),
            },
            {
                "text": "Company",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Company": self.menu_callback(x),
            },
            {
                "text": "Package",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Package": self.menu_callback(x),
            },
        ]
        self.menu = MDDropdownMenu(
            caller = self.ids.dropdown_item,
            items=menu_items,
            width_mult=4,
            max_height = 150
        )
    
    def full_details(self,row_id):
        # shows all details of offer letter in a dialog box
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


    def menu_callback(self, text_item):
        self.ids.dropdown_item.text = text_item
        self.menu.dismiss()