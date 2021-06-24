from kivy.uix.screenmanager import Screen
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import flags
from datetime import date

class DepartmentLevel(Screen):
    def __init__(self,**kw):
        super(DepartmentLevel, self).__init__(**kw)

    def pie_chart(self):
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        my_cursor.execute(f"select co.name,count(co.name) from offer_letters as ol inner join company as co on ol.company_id = co.company_id inner join students as st on ol.enrollment_id = st.enrollment_id where co.branch = {branch} and st.pass_year = year(curdate()) group by co.name;")
        records = my_cursor.fetchall()
        labels,values = [i[0] for i in records],[i[1] for i in records]
        # plotting
        plt.title(f"Offer Letters by company in {date.today().year}")
        plt.pie(values,labels=labels,autopct='%1.1f%%')
        plt.axis("equal")
        plt.show()
    
    def double_bar(self):
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        my_cursor.execute(f"select st.pass_year, count(st.enrollment_id) as total, (select count(offer_letters.enrollment_id) from offer_letters inner join students on offer_letters.enrollment_id=students.enrollment_id where offer_letters.finalised='' and students.pass_year = st.pass_year and students.branch={branch}) as placed from students as st where st.branch = {branch} and st.pass_year between year(curdate())-3 and year(curdate()) group by pass_year order by st.pass_year desc limit 3;")
        records = my_cursor.fetchall()
        labels = [i[0] for i in records]
        no_of_students =[i[1] for i in records]
        placed_students = [i[2] for i in records]
        x_axis = np.arange(len(records))
        y_ticks = np.arange(max(no_of_students)+5,step=5)
        plt.bar(x_axis-0.2,no_of_students,0.4,label='total')
        plt.bar(x_axis+0.2,placed_students,0.4,label='placed')
        plt.xticks(x_axis,labels)
        plt.yticks(y_ticks)
        plt.xlabel("Year")
        plt.ylabel("Number of students")
        plt.legend()
        plt.show()

    def multiple_bar(self):
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        my_cursor.execute(f"select co.name,st.pass_year from offer_letters inner join company as co on offer_letters.company_id=co.company_id inner join students as st on offer_letters.enrollment_id=st.enrollment_id where st.branch={branch} and st.pass_year between year(curdate())-3 and year(curdate());")
        dat=[]
        data = my_cursor.fetchall()
        for i in data:
            dat.append([i[0],i[1]])
        df=pd.DataFrame(dat,columns=['company','year'])
        sns.countplot(x=df['company'],hue=df['year'])
        plt.title("Offer Letters by companies")
        plt.xlabel("Companies")
        plt.ylabel("Number of offer letters")
        plt.legend()
        plt.show()

    def line_plot(self):
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        dat=[]
        my_cursor.execute(f'select co.package,count(st.pass_year),st.pass_year from offer_letters inner join company as co on offer_letters.company_id=co.company_id inner join students as st on offer_letters.enrollment_id=st.enrollment_id where st.branch={branch} and st.pass_year between year(curdate())-3 and year(curdate()) group by co.package, st.pass_year;')
        for i in my_cursor:
                dat.append([i[0],i[1],i[2]])
        df=pd.DataFrame(dat,columns=['package','count','year'])

        sns.lineplot(x='package',y='count',hue = 'year',data=df)
        plt.title("Count of Package")
        plt.yticks(np.arange(max(df['count'])+5,step=5))
        plt.xlabel("Package")
        plt.ylabel("Count")
        plt.legend()
        plt.show()