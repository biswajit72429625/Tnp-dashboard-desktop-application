from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import flags



class InstituteTableTitleLabel(MDLabel):
    text = StringProperty()
class InstituteTableLabel(MDLabel):
    text = StringProperty()


class InstituteAnalysis(Screen):
    def __init__(self, **kw):
        super(InstituteAnalysis,self).__init__(**kw)

    def prepare_graphs(self):
        self.countplt()
        self.placedstat()
        graphs=self.manager.get_screen('institute_graphs')
        # reload images
        for i in range(1,3):
            graphs.ids[str(i)].reload()

    def load_analysis(self):
        for k,v in flags.branch.items():
            if v==flags.app.officer_branch:
                branch=k
                break
        my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
        # retriving list of packages
        
        my_cursor.execute('''select distinct(co.package)
                        from offer_letters as ol
                        inner join company as co on ol.company_id = co.company_id
                        inner join students as st on ol.enrollment_id = st.enrollment_id
                        where st.pass_year = year(curdate());''')
        packages = my_cursor.fetchall()
        for package in packages:
            # add package
            self.ids.grid.add_widget(InstituteTableTitleLabel(text=str(package[0])))
            # add offer count, placed count
            my_cursor.execute(f"select count(st.enrollment_id) as offers, (select count(std.enrollment_id) from offer_letters as ol inner join company as co on ol.company_id = co.company_id inner join students as std on ol.enrollment_id = std.enrollment_id where std.pass_year = year(curdate()) and co.package = {float(package[0])} and ol.finalised = '') as placed from offer_letters as ol inner join company as co on ol.company_id = co.company_id inner join students as st on ol.enrollment_id = st.enrollment_id where st.pass_year = year(curdate()) and co.package = {float(package[0])};")
            offer,placed = my_cursor.fetchall()[0]
            self.ids.grid.add_widget(InstituteTableLabel(text=str(offer)))
            self.ids.grid.add_widget(InstituteTableLabel(text=str(placed)))
            for branch in range(1,7):
                # count of students placed for given for package and branch
                my_cursor.execute(f"select count(st.enrollment_id) as offers from offer_letters as ol inner join company as co on ol.company_id = co.company_id inner join students as st on ol.enrollment_id = st.enrollment_id where st.pass_year = year(curdate()) and co.package = {float(package[0])} and st.branch={branch} and ol.finalised = '';")
                self.ids.grid.add_widget(InstituteTableLabel(text=str(my_cursor.fetchall()[0][0])))

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
        dat=[]
        my_cursor.execute('select st.branch, st.pass_year from offer_letters as ol inner join students as st on ol.enrollment_id=st.enrollment_id where st.pass_year between year(curdate())-3 and year(curdate());')
        for i in my_cursor:
            dat.append([branch[i[0]],i[1]])
        df=pd.DataFrame(dat,columns=['branch','year'])
        sns.countplot(x=df['branch'],hue=df['year'])
        # plt.show()
        plt.savefig("Graphs//inst_1.png")
        plt.close('all')
    
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
        # plt.show()
        plt.savefig("Graphs//inst_2.png")
        plt.close('all')

    # def multiple_bar(self):
    #     for k,v in flags.branch.items():
    #         if v==flags.app.officer_branch:
    #             branch=k
    #             break
    #     my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
    #     my_cursor.execute(f"select co.name,st.pass_year from offer_letters inner join company as co on offer_letters.company_id=co.company_id inner join students as st on offer_letters.enrollment_id=st.enrollment_id where st.branch={branch} and st.pass_year between year(curdate())-3 and year(curdate());")
    #     dat=[]
    #     data = my_cursor.fetchall()
    #     for i in data:
    #         dat.append([i[0],i[1]])
    #     df=pd.DataFrame(dat,columns=['company','year'])
    #     sns.countplot(x=df['company'],hue=df['year'])
    #     plt.title("Offer Letters by companies")
    #     plt.xlabel("Companies")
    #     plt.ylabel("Number of offer letters")
    #     plt.legend()
    #     # plt.show()
    #     plt.savefig("Graphs//dept_3.png")
    #     plt.close('all')

    # def line_plot(self):
    #     for k,v in flags.branch.items():
    #         if v==flags.app.officer_branch:
    #             branch=k
    #             break
    #     my_db, my_cursor = self.manager.my_db, self.manager.my_cursor
    #     dat=[]
    #     my_cursor.execute(f'select co.package,count(st.pass_year),st.pass_year from offer_letters inner join company as co on offer_letters.company_id=co.company_id inner join students as st on offer_letters.enrollment_id=st.enrollment_id where st.branch={branch} and st.pass_year between year(curdate())-3 and year(curdate()) group by co.package, st.pass_year;')
    #     for i in my_cursor:
    #             dat.append([i[0],i[1],i[2]])
    #     df=pd.DataFrame(dat,columns=['package','count','year'])

    #     sns.lineplot(x='package',y='count',hue = 'year',data=df)
    #     plt.title("Count of Package")
    #     plt.yticks(np.arange(max(df['count'])+5,step=5))
    #     plt.xlabel("Package")
    #     plt.ylabel("Count")
    #     plt.legend()
    #     # plt.show()
    #     plt.savefig("Graphs//dept_4.png")
    #     plt.close('all')


class InstituteGraphs(Screen):
    def __init__(self, **kw):
        super(InstituteGraphs, self).__init__(**kw)
