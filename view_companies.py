from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from database import db_connector
import flags

class CompanyDialog(BoxLayout):
    pass

class ViewCompanies(Screen):
    dialog = None
    def __init__(self, **kw):
        super(ViewCompanies, self).__init__(**kw)
    
    def full_details(self,row_id):
        # shows all details of e_resource in a dialog box
        self.dialog = MDDialog(
            title=str(self.ids[f'{str(row_id)}'].text),
            type="custom",
            content_cls=CompanyDialog(),
            buttons=[
                    MDRoundFlatButton(text="CANCEL",on_press=self.dismiss_dialog),
                    MDRoundFlatButton(text="SAVE"),
                ]
        )
        self.dialog.open()

    def dismiss_dialog(self,instance):
        self.dialog.dismiss()

    def menu_for_add_company(self):
        my_db, my_cursor = db_connector()
        query = f"select Distinct(role) from company ;"
        my_cursor.execute(query)
        self.menu = my_cursor.fetchall()
        #print(self.menu)
        self.menu_items = []
        for i in self.menu:
            temp = {
                
                "text": i[0],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i[0]: self.menu_callback(x),
            }
            self.menu_items.append(temp)
        temp = {
                
                "text": "other",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="other": self.menu_callback(x),
            }
        self.menu_items.append(temp)
        #print(self.menu_items)
        # flags.add_company_role_menu_item = self.menu_items
        #print(flags.add_company_role_menu_item)this is printing correct , flags tak sab theek jara hai
        self.menu = MDDropdownMenu(
            caller = self.manager.get_screen('add_companies').ids.dropdown_item,
            items=self.menu_items,
            width_mult=4,
            max_height = 300
        )
    def menu_callback(self, text_item):
        # sets dropdown wale as text of button and closes dropdown menu
        self.manager.get_screen('add_companies').ids.dropdown_item.text = text_item
        self.manager.get_screen('add_companies').ids.role.text = text_item
        self.menu.dismiss()
        if self.manager.get_screen('add_companies').ids.dropdown_item.text == "other":
            self.manager.get_screen('add_companies').ids.role.text = ""
            self.manager.get_screen('add_companies').ids.role.disabled = False
        else:
            self.manager.get_screen('add_companies').ids.role.disabled = True
            self.manager.get_screen('add_companies').ids.role.text = text_item
    def add_delete(self,instance):
        if instance.icon == 'notebook-plus-outline':
            self.menu_for_add_company()
            self.manager.current = 'add_companies'
            self.manager.stack.append(self.name)
        else:
            pass
    