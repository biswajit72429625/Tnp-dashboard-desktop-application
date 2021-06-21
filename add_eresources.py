from kivy.uix.screenmanager import Screen
from kivymd.uix.picker import MDDatePicker,MDTimePicker 
from kivymd.uix.menu import MDDropdownMenu
from database import show_alert_dialog,db_connector
from datetime import datetime, date
import flags
class AddEresources(Screen):
    def __init__(self, **kw):
        super(AddEresources,self).__init__(**kw)
        today = date.today()
        self.menu_items = [
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
            items=self.menu_items,
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
        else:
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
        self.year=self.ids.dropdown_item.text
        self.eorganizer=self.ids.e_organiser.text
        self.elink=self.ids.e_link.text
        date=self.ids.date_label.text
        time=self.ids.time_label.text
        date_time = date+' '+time                                
#to check the constraints
        if len(self.ename) > 20 or len(self.ename)==0:
            show_alert_dialog(self,"Title should be in range 0-20!!")
        elif len(self.eorganizer) > 60 or len(self.eorganizer)==0:
            show_alert_dialog(self,"Organiser should be in range 0-60")
        elif len(self.elink)==0:
            show_alert_dialog(self,"Please Provide the link!!!")
        elif self.ids.dropdown_item.text=='Passing Year':
            show_alert_dialog(self,"Please Provide passing year!!!")
        elif (self.ids.checkbox_id.active==False) and (date=='Select Date' or time=='Select Time') :
            show_alert_dialog(self,"Please Select the date and time!!!")
        if date_time!='Select Date Select Time':
            self.date= datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S")
       #connecting to database
        my_db, my_cursor = db_connector()
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        #checking description and checkbox 
        if (self.ids.checkbox_id.active==True) and len(self.ids.e_description.text)!=0:
            qur='insert into e_resources (title , pass_year , branch ,organizer, link , description) values (%s,%s,%s,%s,%s,%s)'
        
            val=(self.ename,self.year,branch,self.eorganizer,self.elink,str(self.ids.e_description.text))
            
            
            
        elif (self.ids.checkbox_id.active==False) and len(self.ids.e_description.text)!=0:
            qur='insert into e_resources (title , pass_year , branch ,organizer, link , visible,description) values (%s,%s,%s,%s,%s,%s,%s)'
        
            val=(self.ename,self.year,branch,self.eorganizer,self.elink,self.date,self.ids.e_description.text)
           
        elif (self.ids.checkbox_id.active==False) and len(self.ids.e_description.text)==0:
            qur='insert into e_resources (title , pass_year , branch ,organizer, link,visible ) values (%s,%s,%s,%s,%s,%s)'
        
            val=(self.ename,self.year,branch,self.eorganizer,self.elink,self.date)
            
            
            
        
        elif (self.ids.checkbox_id.active==True) and len(self.ids.e_description.text)==0:
            qur='insert into e_resources (title , pass_year , branch ,organizer, link  ) values (%s,%s,%s,%s,%s)'
        
            val=(self.ename,self.year,branch,self.eorganizer,self.elink)
            
            
        my_cursor.execute(qur,val)
        my_db.commit()
        show_alert_dialog(self,"EResources added  Sucessfully !!!")
        self.manager.callback()
        self.manager.callback()
        
                
    def clear(self):#to clear all fields
        self.ids.e_name.text=''
        self.ids.e_organiser.text=''
        self.ids.e_link.text=''
        self.ids.e_description.text=''
        self.ids.dropdown_item.text='Passing Year'
        self.ids.checkbox_id.active=False
        self.ids.date_label.text='Select Date'
        self.ids.time_label.text='Select Time'
        
        

        
        