# from functools import partialmethod
from kivy.uix.screenmanager import Screen
from kivymd.uix.filemanager import MDFileManager
from database import db_connector,show_alert_dialog
from datetime import datetime, date
import flags
import os
import pandas as pd


class FinalizeOffer(Screen):
    def __init__(self, **kw):
        super(FinalizeOffer, self).__init__(**kw)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager = self.exit_manager,
            select_path = self.select_path,
            # preview = True
            ext=[".xlsx",".csv",".txt",".xls"]
        )
    
    

    def file_manager_open(self):
        try:
            os.makedirs(f"C:\\Users\\{os.getlogin()}\\Downloads\\tnp")
        except FileExistsError:
            pass
        
        self.file_manager.show(f"C:\\Users\\{os.getlogin()}\\Downloads\\tnp")
        self.manager_open = True

    def select_path(self, path):
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        df=pd.read_excel(path)
        enroll=list(df['enrollment id'])
        comp=list(df['company name'])
        role=list(df['role'])
        br=list(df['branch'])
        brid=[]
        for i in br:
            for k,v in flags.branch.items():
                if v==i:
                    brid.append(k)
                    break        

        for i in range(len(enroll)):

            qu="update offer_letters set finalised='' where enrollment_id=%s and company_id=(select company_id from company where name=%s and role=%s and branch = %s) ;"
            va=(enroll[i],comp[i],role[i],brid[i])
            print(enroll[i],comp[i],role[i],brid[i])
            my_cursor.execute(qu,va)
            my_db.commit()
        show_alert_dialog(self,'Database Updated!!!')

        self.exit_manager()
        


    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''
        
        self.manager_open = False
        self.file_manager.close()
    
    

        