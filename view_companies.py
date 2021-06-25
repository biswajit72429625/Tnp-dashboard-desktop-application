from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from database import show_alert_dialog, disable_toggler
from functools import partial
import flags

class CompanyDialog(BoxLayout):
    def __init__(self,role_list,**kw):
        super(CompanyDialog, self).__init__(**kw)
        self.menu = MDDropdownMenu(
            caller = self.ids.dialog_role_spinner,
            items=role_list,
            width_mult=4,
            max_height = 200
            )


class ViewCompanies(Screen):
    def __init__(self, **kw):
        super(ViewCompanies, self).__init__(**kw)
    
    def full_details(self,row_id):
        # shows all details of e_resource in a dialog box
        self.id = int(row_id)
        self.records = self.manager.get_screen('placements').company_records[self.id]
        # for fetching list of roles form db and giving a dropdown menu
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        query = f"select Distinct(role) from company ;"
        my_db.ping(reconnect=True)
        my_cursor.execute(query)
        self.menu = my_cursor.fetchall()
        #print(self.menu)
        self.menu_items = []
        for i in self.menu:
            temp = {
                
                "text": i[0],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i[0]: self.edit_menu_callback(x),
            }
            self.menu_items.append(temp)
        temp = {
                
                "text": "other",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="other": self.edit_menu_callback(x),
            }
        self.menu_items.append(temp)
        # creating instance of of dialog box, fill in data and disable everything
        self.dialog_data = CompanyDialog(self.menu_items)
        self.dialog_data.ids.dialog_package.text = str(self.records[2])
        if self.records[3] == '':
            self.dialog_data.ids.dialog_platform.text = "On-Campus"
        else:
            self.dialog_data.ids.dialog_platform.text = "Off-Campus"
        self.dialog_data.ids.dialog_website.text = self.records[4]
        self.dialog_data.ids.dialog_role_spinner.text = self.records[5]
        self.dialog_data.ids.dialog_role_text.text = self.records[5]
        self.dialog_data.ids.dialog_branch.text = flags.branch[self.records[6]]
        self.all_id = ['dialog_package','dialog_platform','dialog_website','dialog_role_spinner','dialog_role_text','dialog_branch']
        # disabling data
        disable_toggler(self.dialog_data,self.all_id,True)
        self.dialog = MDDialog(
            title=self.records[1],
            type="custom",
            content_cls=self.dialog_data,
            buttons=[
                    MDRoundFlatButton(text="CANCEL",on_press=self.dismiss_dialog),
                    MDRoundFlatButton(text="SAVE",on_press=self.save_dialog),
                ]
        )
        self.dialog.open()

    def edit_menu_callback(self, text_item):
        # sets dropdown wale as text of button and closes dropdown menu
        self.dialog_data.ids.dialog_role_spinner.text = text_item
        if text_item == 'other':
            self.dialog_data.ids.dialog_role_text.disabled = False
            self.dialog_data.ids.dialog_role_text.text = ""
        else:
            self.dialog_data.ids.dialog_role_text.disabled = True
            self.dialog_data.ids.dialog_role_text.text = text_item
        self.dialog_data.menu.dismiss()

    def dismiss_dialog(self,instance):
        # dismisses full details dialog
        self.dialog.dismiss()

    def menu_for_add_company(self):
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        query = f"select Distinct(role) from company ;"
        my_db.ping(reconnect=True)
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
        # speeddial options
        if instance.icon == 'notebook-plus-outline':
            self.menu_for_add_company()
            self.manager.current = 'add_companies'
            self.manager.stack.append(self.name)
        else:
            self.delete_companies()

    def edit_company(self):
        # enable all data except branch
        abc = self.all_id[:-2]
        disable_toggler(self.dialog_data,abc,False)

    def save_dialog(self,instance):
        #  if widgets are not disabled, modify the database
        if not self.dialog_data.ids.dialog_package.disabled:
            self.package = self.dialog_data.ids.dialog_package.text
            self.platform = self.dialog_data.ids.dialog_platform.text
            self.website = self.dialog_data.ids.dialog_website.text
            self.role = self.dialog_data.ids.dialog_role_text.text
            # checking constraints
            try: # package constraint
                self.package = float(self.package)
            except ValueError:
                show_alert_dialog(self.dialog_data,"Enter valid package `number.number`")
                return
            if len(self.website) == 0: # website constraint
                show_alert_dialog(self.dialog_data,"Please enter website")
                return
            if len(self.role) == 0 or len(self.role) > 50: # role constraints
                show_alert_dialog(self.dialog_data,"Please enter role in length range 1-50")
                return
            if self.platform == "On-Campus": # setting platform
                self.platform = ''
            else:
                self.platform = None
            # connecting to database
            # my_db, my_cursor = db_connector()
            my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
            query = f"UPDATE company SET package = %s, platform = %s, website = %s, role = %s where company_id = %s"
            values = (self.package, self.platform, self.website, self.role, self.records[0])
            my_db.ping(reconnect=True)
            my_cursor.execute(query,values)
            my_db.commit()
            # closing dialog
            self.dismiss_dialog(self.dialog)
            # showing message as modified successfully
            show_alert_dialog(self,"Modified company successfully")
            # going back to placements page
            self.manager.callback()
        else:
            # else close dialog
            self.dismiss_dialog(self.dialog)
            
    def delete_companies(self):
        # asks if confirm delete?
        checks = self.manager.get_screen('placements').company_checkbox_list # list of checkboxes checked
        records = self.manager.get_screen('placements').company_records # list of all records
        self.delete_dialog = MDDialog(
        text="Sure Delete?",
        buttons=[
            MDRoundFlatButton(text="CANCEL",on_press=self.dismiss_delete_dialog),
            MDRoundFlatButton(text="SURE",on_press=partial(self.confirm_delete_dialog,checks,records)),
        ],
        )
        self.delete_dialog.open()

    def dismiss_delete_dialog(self,instance):
        # dismiss delete dialog box
        self.delete_dialog.dismiss()

    def confirm_delete_dialog(self,checks,records,instance):
        # confirm delete from database
        self.dismiss_delete_dialog(self.delete_dialog)
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        my_db.ping(reconnect=True)
        for i in checks: 
            if i.active:
                my_cursor.execute(f'DELETE FROM company WHERE company_id={records[int(i.id)][0]};')
        my_db.commit()
        show_alert_dialog(self,"Company deleted")
        self.manager.callback()
