from kivy.uix.screenmanager import Screen
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.menu import MDDropdownMenu
from datetime import date
from database import show_alert_dialog, send_mail
import flags


class AddAssessments(Screen):
    def __init__(self, **kw):
        super(AddAssessments, self).__init__(**kw)
        today = date.today()
        menu_items = [
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
            items=menu_items,
            width_mult=4,
            max_height = 200
        )
    def checkbox(self,instance,value):
        if value == True: 
            self.ids.date_label.disabled = True
            self.ids.time_label.disabled = True
        if value == False:
            self.ids.date_label.disabled = False
            self.ids.time_label.disabled = False

    def menu_callback(self, text_item):
        # sets dropdown wale as text of button and closes dropdown menu
        self.ids.dropdown_item.text = text_item
        self.menu.dismiss()
    def show_date_picker(self):
        date_dialog = MDDatePicker(year=2021,month=2,day=14)
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    def on_save(self,instance,value,range):
        self.ids.date_label.text = str(value)
        self.date=self.ids.date_label.text
    def on_cancel(self,*args):
        pass
    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()
    def get_time(self,args,value):
        self.ids.time_label.text = str(value)


    def save(self):
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
            return

        if len(self.eorganizer) > 60 or len(self.eorganizer)==0:
            show_alert_dialog(self,"Organiser should be in range 0-60")
            return

        if len(self.elink)==0:
            show_alert_dialog(self,"Please Provide the link!!!")
            return

        if self.ids.dropdown_item.text=='Passing Year':
            show_alert_dialog(self,"Please Provide passing year!!!")
            return

        if (self.ids.checkbox_id.active==False) and (date=='Select Date' or time=='Select Time') :
            show_alert_dialog(self,"Please Select the date and time!!!")
            return

        '''if 'Select Date' or 'Select Time' not in date_time:
            self.date= datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S")
        else:
            show_alert_dialog(self,"Please Select the date and time!!!")
            return'''

       #connecting to database
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        # print (self.ename,self.eorganizer,self.elink,self.year,branch)
        
        #checking description and checkbox 
        if self.ids.checkbox_id.active==True:
            qur='insert into assessment (title , pass_year , branch ,organizer, link ) values (%s,%s,%s,%s,%s)'
        
            val=(self.ename,self.year,branch,self.eorganizer,self.elink)
        else :
            qur='insert into assessment (title , pass_year , branch ,organizer, link , visible) values (%s,%s,%s,%s,%s,%s)'
        
            val=(self.ename,self.year,branch,self.eorganizer,self.elink,self.date)
        my_db.ping(reconnect=True)
        my_cursor.execute(qur,val)
        my_db.commit()
        # send_mail(self,"New Assessment!",f"By:- {self.eorganizer}\nTopic:- {self.ename}\nLink:- {self.elink}\nTest Time:- {self.date}\nGood Luck with Test",self.year)
        send_mail(self,"New Assessment!",f"By:- {self.eorganizer}\nTopic:- {self.ename}\nLink:- {self.elink}\nGood Luck with Test",self.year)
        show_alert_dialog(self,"Assessments added  Sucessfully !!!")
        self.manager.callback()
        self.manager.callback()
        
        
    def clear(self):
        self.ids.e_name.text=''
        self.ids.e_organiser.text=''
        self.ids.e_link.text=''
        self.ids.dropdown_item.text='Passing Year'
        self.ids.checkbox_id.active=False
        self.ids.date_label.text='Select Date'
        self.ids.time_label.text='Select Time'
        
    def change_field(self,kivy_id):
        # changes focus to next text on pressing enter
        self.ids[kivy_id].focus=True
