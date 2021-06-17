from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu

class TpoRegister(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        # menu_items = [{"text" : 'CSE'},{"text" : 'IT'},{"text" : 'ENTC'},{"text" : 'CIVIL'},{"text" : 'MECH'},{"text" : 'ELN'}]
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
        # self.menu.bind(on_release=self.set_item)

    def menu_callback(self, text_item):
        self.ids.dropdown_item.text = text_item
        self.menu.dismiss()

    # def set_item(self,instance_menu,instance_menu_item):
    #     self.ids.dropdown_item.set_item(instance_menu_item.text)
    #     instance_menu.dismiss()
