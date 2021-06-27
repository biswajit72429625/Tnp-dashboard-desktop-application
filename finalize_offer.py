# from functools import partialmethod
from kivy.uix.screenmanager import Screen
from kivymd.uix.filemanager import MDFileManager
from database import show_alert_dialog
import flags
import os
import pandas as pd
from mysql.connector.errors import InterfaceError


class FinalizeOffer(Screen):
    def __init__(self, **kw):
        super(FinalizeOffer, self).__init__(**kw)
        # file manager part
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager = self.exit_manager,
            select_path = self.select_path,
            # preview = True
            ext=[".xlsx",".csv",".txt",".xls"]
        )

    def file_manager_open(self):
        # creating path of dosnt exists
        try:
            os.makedirs(f"C:\\Users\\{os.getlogin()}\\Downloads\\tnp")
        except FileExistsError:
            pass
        # open path
        self.file_manager.show(f"C:\\Users\\{os.getlogin()}\\Downloads\\tnp")
        self.manager_open = True

    def select_path(self, path):
        # retrive csv file path
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        df=pd.read_excel(path)
        # preparing dataframe
        enroll=list(df['enrollment id'])
        comp=list(df['company name'])
        role=list(df['role'])
        # getting officer branch
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break        
        # pinging database to check for network connection
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        for i in range(len(enroll)):
            # upating database
            qu="update offer_letters set finalised='' where enrollment_id=%s and company_id=(select company_id from company where name=%s and role=%s and branch = %s) ;"
            va=(enroll[i],comp[i],role[i],branch)
            # print(enroll[i],comp[i],role[i],branch)
            my_cursor.execute(qu,va)
            my_db.commit()
        show_alert_dialog(self,'Database Updated!!!')
        # close file manager
        self.exit_manager()
        


    def exit_manager(self, *args):
        # close file manager
        self.manager_open = False
        self.file_manager.close()
    
    

        