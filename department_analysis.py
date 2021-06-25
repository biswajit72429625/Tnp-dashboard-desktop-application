from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import flags
from datetime import date



class DepartmentTableTitleLabel(MDLabel):
    text = StringProperty()
class DepartmentTableLabel(MDLabel):
    text = StringProperty()

class DepartmentGridYear(GridLayout):
    def __init__(self,**kw):
        super(DepartmentGridYear, self).__init__(**kw)
class DepartmentAnalysis(Screen):
    def __init__(self, **kw):
        super(DepartmentAnalysis,self).__init__(**kw)

    def prepare_graphs(self):
        self.pie_chart()
        self.double_bar()
        self.multiple_bar()
        self.line_plot()
        graphs=self.manager.get_screen('department_graphs')
        # reload images
        for i in range(1,5):
            graphs.ids[str(i)].reload()

    def load_analysis(self):
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        # retriving roles
        my_cursor.execute(f"select distinct(co.role) from offer_letters as ol inner join company as co on ol.company_id=co.company_id inner join students as st on ol.enrollment_id=st.enrollment_id where st.branch = {branch};")
        roles = my_cursor.fetchall()
        self.ids.grid.clear_widgets()
        self.ids.grid.cols = len(roles)+1
        # adding first blank column
        self.ids.grid.add_widget(DepartmentTableTitleLabel())
        # adding roles
        for role in roles:
            self.ids.grid.add_widget(DepartmentTableTitleLabel(text=role[0]))
        # adding second blank column
        self.ids.grid.add_widget(DepartmentTableTitleLabel())
        # adding grid of years to all roles
        for _ in range(len(roles)):
            # creating grid for past 3 years
            temp = DepartmentGridYear()
            for i in range(3):
                temp.add_widget(DepartmentTableTitleLabel(text=str(date.today().year-i)))
            self.ids.grid.add_widget(temp)
        years = [date.today().year,date.today().year-1,date.today().year-2]
        # retriving list of companies
        my_cursor.execute(f"select distinct(co.name) from offer_letters as ol inner join company as co on ol.company_id=co.company_id inner join students as st on ol.enrollment_id=st.enrollment_id where st.branch = {branch};")
        companies = my_cursor.fetchall()
        for company in companies:
            # add company
            self.ids.grid.add_widget(DepartmentTableTitleLabel(text=company[0]))
            for role in roles:
                # 3 column grid of year for each role
                temp = DepartmentGridYear()
                for year in years:
                    # count of students placed for given company, role, year and branch
                    my_cursor.execute(f"select count(ol.enrollment_id) from offer_letters as ol inner join company as co on ol.company_id=co.company_id inner join students as st on ol.enrollment_id = st.enrollment_id where st.branch='{branch}' and st.pass_year = {year} and co.name = '{company[0]}' and co.role = '{role[0]}' and ol.finalised='';")
                    # adding 1 of 3 columns
                    temp.add_widget(DepartmentTableLabel(text=str(my_cursor.fetchall()[0][0])))
                # adding all 3 column grid to main gird
                self.ids.grid.add_widget(temp)

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
        # plt.show()
        plt.savefig("Graphs//dept_1.png")
        plt.close('all')
    
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
        # plt.show()
        plt.savefig("Graphs//dept_2.png")
        plt.close('all')

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
        # plt.show()
        plt.savefig("Graphs//dept_3.png")
        plt.close('all')

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
        # plt.show()
        plt.savefig("Graphs//dept_4.png")
        plt.close('all')


class DepartmentGraphs(Screen):
    def __init__(self, **kw):
        super(DepartmentGraphs, self).__init__(**kw)
