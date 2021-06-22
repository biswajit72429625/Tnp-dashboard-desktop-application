# from functools import partialmethod
from kivy.uix.screenmanager import Screen
from kivymd.uix.filemanager import MDFileManager
from database import show_alert_dialog
# from datetime import datetime, date
# import flags
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
        self.file_manager.show(r'D:\resume')
        self.manager_open = True

    def select_path(self, path):
        # my_db, my_cursor = db_connector()
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        df=pd.read_excel(path)
        enroll=list(df['enrollment id'])
        comp=list(df['company name'])
        role=list(df['role'])
    #student
        cid=[]
        for i in range(0,len(comp)):
            que="select company_id from company where company_id in (select company_id from company where name=%s and role=%s);"
            val=(comp[i],role[i])
            my_cursor.execute(que,val)
            for j in my_cursor:
                cid.append(j[0])
            

            
        
        for i in range(len(enroll)):
            print(i,j)
            qu="update offer_letters set finalised='' where enrollment_id=%s and company_id=%s ;"
            va=(enroll[i],cid[i])
            my_cursor.execute(qu,va)
            my_db.commit()
        show_alert_dialog(self,'Database Updated!!!')
            
        


            

        
        
        

        self.exit_manager()
        print(path)


    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''
        
        self.manager_open = False
        self.file_manager.close()
    
    

        