from kivy.uix.screenmanager import Screen
from database import show_alert_dialog
from mysql.connector.errors import InterfaceError
import re
import flags

class AddCompanies(Screen):
    def __init__(self, **kw):
        super(AddCompanies, self).__init__(**kw)
    
    def clear(self):
        #to clear all fields
        self.ids.name.text=''
        self.ids.link.text=''
        self.ids.package.text=''
        self.ids.dropdown_item.text='Choose Role'
        self.ids.type.text='Placement Type'
        self.ids.role.text=''
    
    def verify(self):
        # checking all the constraints
        nam=self.ids.name.text
        website=self.ids.link.text
        package=self.ids.package.text
        type=self.ids.type.text
        role=self.ids.role.text

        if (len(nam )==0 or len(nam)>60): # name length
            show_alert_dialog(self,"Enter name in range 1-60!!!")
            return
        if len(nam.split())>0: # name type
            l=nam.split()
            for i in l:
                if not re.match(r"([a-zA-Z.])",i):
                    show_alert_dialog(self,"Please enter valid name!!!")
                    return
                    

        if len(website)==0:
            show_alert_dialog(self,"Please Provide the Website!!!")
            return
        try:
            package=float(package)
        except ValueError:
            show_alert_dialog(self,"Please enter valid package")
            return    
        if type=="Placement Type":#check dpartment
            show_alert_dialog(self,"Please Select Placement Type")
            return 
        
        if self.ids.dropdown_item.text=="other":
            if role=="":
                show_alert_dialog(self,"Please Type Role")
                return
        if self.ids.dropdown_item.text=="Choose Role" :#check dpartment
            show_alert_dialog(self,"Please Select Role")
            return
        
        if type == "On-campus":
            type = ''
        else:
            type = None
        # connecting to database
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        quer="SELECt company_id from company where name = %s and package = %s and role = %s and platform = %s and branch = %s"
        # pinging database to check connection
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        my_cursor.execute(quer,(nam,package,role,type,branch))
        if my_cursor.fetchall():
            show_alert_dialog(self,"company already exists")
        else:
            query="insert into company (name,package,platform,website,role,branch) values (%s ,%s, %s ,%s,%s,%s);"
            values = (nam,package,type,website,role,branch)
            my_cursor.execute(query,values)
            my_db.commit()
            show_alert_dialog(self,"Data Sucessfully Saved!!!")
            # changing screen
            self.manager.callback()
            self.manager.callback()

    def change_field(self,kivy_id):
        # changes focus to next text on pressing enter
        self.ids[kivy_id].focus=True