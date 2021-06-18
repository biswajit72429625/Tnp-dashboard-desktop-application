from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.dialog import MDDialog
from database import db_connector
import flags

class EResourceDialog(BoxLayout):
    pass

class ViewEresources(Screen):
    dialog = None
    def __init__(self, **kw):
        super(ViewEresources, self).__init__(**kw)
    
    def full_details(self,id):
        # shows all details of e_resource in a dialog box
        my_db, my_cursor = db_connector()
        # get records from home_screen
        records = self.manager.get_screen('home_page').eresources_records[int(id)]
        # create insatance of dialog box,  fill in data and disable everything
        dialog_data = EResourceDialog()
        dialog_data.ids.dialog_passyear.text = records[2]
        dialog_data.ids.dialog_branch.text = flags.branch[records[3]]
        dialog_data.ids.dialog_organizer.text = records[4]
        dialog_data.ids.dialog_link.text = records[5]
        dialog_data.ids.dialog_visible.text = str(records[6])
        dialog_data.ids.dialog_description.text = records[7]
        dialog_data.ids.dialog_passyear.disabled = True
        dialog_data.ids.dialog_branch.disabled = True
        dialog_data.ids.dialog_organizer.disabled = True
        dialog_data.ids.dialog_link.disabled = True
        dialog_data.ids.dialog_visible.disabled = True
        dialog_data.ids.dialog_description.disabled = True

        # create dialog box
        self.dialog = MDDialog(
            title="1",
            type="custom",
            content_cls=dialog_data,
            buttons=[
                    MDRoundFlatButton(text="CANCEL",on_press=self.dismiss_dialog),
                    MDRoundFlatButton(text="SAVE"),
                ]
        )
        self.dialog.open()

    def dismiss_dialog(self,instance):
        # dismiss dialog box
        self.dialog.dismiss()

    def add_delete(self,instance):
        # speeddial button instance
        if instance.icon == 'notebook-plus-outline':
            self.manager.current = 'add_eresources'
            self.manager.stack.append(self.name)
        else:
            pass