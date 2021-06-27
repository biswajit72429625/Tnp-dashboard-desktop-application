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
from mysql.connector.errors import InterfaceError
from database import show_alert_dialog


class DepartmentTableTitleLabel(MDLabel):
    # department screen title label
    text = StringProperty()
class DepartmentTableLabel(MDLabel):
    # department screen label
    text = StringProperty()

class DepartmentGridYear(GridLayout):
    # department grid year label
    def __init__(self,**kw):
        super(DepartmentGridYear, self).__init__(**kw)

class DepartmentGraphs(Screen):
    # graphs screen
    def __init__(self, **kw):
        super(DepartmentGraphs, self).__init__(**kw)

class DepartmentAnalysis(Screen):
    # department detail analysis screen
    def __init__(self, **kw):
        super(DepartmentAnalysis,self).__init__(**kw)

    def load_analysis(self):
        # load detail analysis of department level
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        # pinging to database for network issue
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        # retriving roles
        my_cursor.execute(f"select distinct(co.role) from offer_letters as ol inner join company as co on ol.company_id=co.company_id inner join students as st on ol.enrollment_id=st.enrollment_id where st.branch = {branch};")
        roles = my_cursor.fetchall()
        self.ids.grid.clear_widgets()
        # changing number of column based on number of roles
        self.ids.grid.cols = len(roles)+1
        # adding first blank column
        self.ids.grid.add_widget(DepartmentTableTitleLabel())
        # adding roles
        for role in roles:
            self.ids.grid.add_widget(DepartmentTableTitleLabel(text=role[0]))
        # adding second blank column
        self.ids.grid.add_widget(DepartmentTableTitleLabel(text="Companies"))
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

    
class DepartmentBasicDetails(Screen):
    def __init__(self, **kw):
        super(DepartmentBasicDetails,self).__init__(**kw)

    def load_basic_details(self):
        # loads basic details
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        self.ids.grid.clear_widgets()
        # retriving list of companies
        # pinging database to check for network connection
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        # retriving list of companies
        my_cursor.execute(f'''select distinct(co.name)
                             from offer_letters as ol 
                             inner join company as co on ol.company_id=co.company_id 
                             inner join students as st on ol.enrollment_id=st.enrollment_id 
                             where st.branch = {branch};''')
        companies = my_cursor.fetchall()
        for company in companies:
            # add company
            self.ids.grid.add_widget(DepartmentTableTitleLabel(text=str(company[0])))
            for i in range(0,3):
                # count of students placed for given for package and branch
                my_cursor.execute(f'''select count(ol.enrollment_id) 
                                from offer_letters as ol 
                                inner join students as st on ol.enrollment_id=st.enrollment_id 
                                inner join company as co on ol.company_id=co.company_id 
                                where st.branch = {branch} and ol.finalised = '' and co.name = '{company[0]}' and st.pass_year=year(curdate())-{i};''')
                self.ids.grid.add_widget(DepartmentTableLabel(text=str(my_cursor.fetchall()[0][0])))

    def load_department(self):
        # switch to full details screen
        department_analysis_screen = self.manager.get_screen("department_analysis")
        department_analysis_screen.load_analysis()

    def prepare_graphs(self):
        # prepares all graphs and reloads it from grphs directory
        self.pie_chart()
        self.double_bar()
        self.multiple_bar()
        self.line_plot()
        graphs=self.manager.get_screen('department_graphs')
        # reload images
        for i in range(1,5):
            graphs.ids[str(i)].reload()

    def pie_chart(self):
        # pie chart for offer letters per company
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        # pinging database to check for network connection
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        # retriving company name and count of same
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
        # double bar graph for total students vs placed students for past 3 years
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        # pinging database to check for network connection
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        # retriving pass_year and count of enrollment id, finalsed count
        my_cursor.execute(f"select st.pass_year, count(st.enrollment_id) as total, (select count(offer_letters.enrollment_id) from offer_letters inner join students on offer_letters.enrollment_id=students.enrollment_id where offer_letters.finalised='' and students.pass_year = st.pass_year and students.branch={branch}) as placed from students as st where st.branch = {branch} and st.pass_year between year(curdate())-3 and year(curdate()) group by pass_year order by st.pass_year desc limit 3;")
        records = my_cursor.fetchall()
        # preparing data
        labels = [i[0] for i in records]
        no_of_students =[i[1] for i in records]
        placed_students = [i[2] for i in records]
        x_axis = np.arange(len(records))
        y_ticks = np.arange(max(no_of_students)+5,step=5)
        # plotting
        plt.bar(x_axis-0.2,no_of_students,0.4,label='total')
        plt.bar(x_axis+0.2,placed_students,0.4,label='placed')
        plt.xticks(x_axis,labels)
        plt.yticks(y_ticks)
        plt.title("Total Placed Students")
        plt.xlabel("Year")
        plt.ylabel("Number of students")
        plt.legend()
        # plt.show()
        plt.savefig("Graphs//dept_2.png")
        plt.close('all')

    def multiple_bar(self):
        # multiple bar graph for offer letters provided by each company for past 3 years
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        # connecting to database
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        # pinging database to check for network connection
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        my_cursor.execute(f"select co.name,st.pass_year from offer_letters inner join company as co on offer_letters.company_id=co.company_id inner join students as st on offer_letters.enrollment_id=st.enrollment_id where st.branch={branch} and st.pass_year between year(curdate())-3 and year(curdate());")
        dat=[]
        # retriving company and year
        data = my_cursor.fetchall()
        for i in data:
            dat.append([i[0],i[1]])
        # preparing data
        df=pd.DataFrame(dat,columns=['company','year'])
        # plotting
        sns.countplot(x=df['company'],hue=df['year'],palette='coolwarm')
        plt.title("Offer Letters by companies")
        plt.xlabel("Companies")
        plt.ylabel("Number of offer letters")
        plt.legend()
        # plt.show()
        plt.savefig("Graphs//dept_3.png")
        plt.close('all')

    def line_plot(self):
        # line plot for number of packages got for past 3 years
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        dat=[]
        # pinging database to check for network connection
        try:
            my_db.ping(reconnect=True,attempts=1)
        except InterfaceError:
            show_alert_dialog(self,"Unable to connect to remote database, due to weak network. Try reconnect after sometime")
            return
        # retriving package count of it and pass_year
        my_cursor.execute(f'select co.package,count(st.pass_year),st.pass_year from offer_letters inner join company as co on offer_letters.company_id=co.company_id inner join students as st on offer_letters.enrollment_id=st.enrollment_id where st.branch={branch} and st.pass_year between year(curdate())-3 and year(curdate()) group by co.package, st.pass_year;')
        for i in my_cursor:
                dat.append([i[0],i[1],i[2]])
        df=pd.DataFrame(dat,columns=['package','count','year'])
        # plotting
        sns.lineplot(x='package',y='count',hue = 'year',data=df,markers=True,style='year')
        plt.title(f"Package Analysis\nmin:-{min(df['package'])}, max:-{max(df['package'])}, avg:- {np.mean(df['package'])}")
        plt.yticks(np.arange(max(df['count'])+5,step=5))
        plt.xlabel("Package")
        plt.ylabel("Offer Count")
        plt.legend()
        # plt.show()
        plt.savefig("Graphs//dept_4.png")
        plt.close('all')

