from kivy.uix.screenmanager import Screen
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from database import db_connector,show_alert_dialog
import pandas as pd


class InstituteLevel(Screen):
    def __init__(self, **kw):
        super(InstituteLevel,self).__init__(**kw)

    def countplt(self):
        branch = {
            1 : "Civil",
            2 : "Mech",
            3 : "CSE",
            4 : "ENTC",
            5 : "ELN",
            6 : "IT"
            }
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        dat=[];brch=[]
        my_cursor.execute('select st.branch, st.pass_year from offer_letters as ol inner join students as st on ol.enrollment_id=st.enrollment_id where st.pass_year between year(curdate())-3 and year(curdate());')
        for i in my_cursor:
            dat.append([branch[i[0]],i[1]])
        df=pd.DataFrame(dat,columns=['branch','year'])
        sns.countplot(x=df['branch'],hue=df['year'])
        plt.show()

    def placedstat(self):
        branch = {
            1 : "Civil",
            2 : "Mech",
            3 : "CSE",
            4 : "ENTC",
            5 : "ELN",
            6 : "IT"
            }
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        brch=[]
        my_cursor.execute('select branch from students ;')
        for i in my_cursor:
            brch.append([branch[i[0]],'Total Students'])
        my_cursor.execute("select branch from students where  enrollment_id  in (select  enrollment_id from offer_letters where finalised='');")
        for i in my_cursor:    
            brch.append([branch[i[0]],'Placed Students'])
        df=pd.DataFrame(brch,columns=['Branch','Placed Status'])
        plt.figure(figsize=(10,6))
        plt.title('students placed per branch')
        sns.countplot(x=df['Branch'],hue=df['Placed Status'])
        plt.show()
                
