from sys import platform
from database import db_connector

my_db, my_cursor = db_connector()
#company =[['infosys','database engineer',4.5,None],['infosys','power programmer',6.2,None],['tcs','database engineer',3.4,None],['tcs','power programmer',8.6,''],['persistent','database engineer',3.8,''],['persistent','power programmer',9.2,''],['wipro','database engineer',4.5,''],['wipro','power programmer',8.5,'']]
qur='insert into offer_letters(enrollment_id ,company_id, link, date_of_interview,date_of_offer ) values (%s,%s,%s,%s,%s)'
#qur='insert into company(name, package, platform,website,role,branch ) values (%s,%s,%s,%s,%s,%s)'
# for i in range(8):
#     val=(company[i][0],company[i][2],company[i][3],'xyz',company[i][1],6)
#     my_cursor.execute(qur,val)
val=(19061040,59,'xyz','2020-07-2','2020-08-28')
my_cursor.execute(qur,val)
my_db.commit()
