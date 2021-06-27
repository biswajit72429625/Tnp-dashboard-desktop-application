import mysql.connector as MYSQL
from decouple import config
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from functools import partial
from email.message import EmailMessage
import smtplib
from difflib import SequenceMatcher
from heapq import nlargest as _nlargest
import flags

def db_connector():
    # connects to database
    my_db = MYSQL.connect(host='remotemysql.com',username=config('remote_user'),passwd=config('remote_passwd'),database='PKuyMx1oEg', port=3306)
    # my_db = MYSQL.connect(host='localhost',username=config('user'),passwd=config('passwd'),database='wit_tnp')
    my_cursor = my_db.cursor()
    return my_db, my_cursor

def show_alert_dialog(self,message):
    # takes message as input and shows error
    self.dialog = MDDialog(
        text=message,
        buttons=[
            MDFlatButton(
                text="Close",on_press=partial(dismiss_dialog,self)
            ),
        ],
    )
    self.dialog.open()

def dismiss_dialog(self,instance):
    # dismiss the dialog
    self.dialog.dismiss()

def disable_toggler(screen,list,value):
    # gets a screen, a list of ids and boolean value and sets diabled value
    for i in list:
        screen.ids[i].disabled = value

def send_mail(screen,subject:str,message:str,year:int):
    # wait message
    # show_alert_dialog(screen,"Please wait informing all students via mail.")
    # getting branch
    for k,v in flags.branch.items():
        if v==flags.app.officer_branch:
            branch=k
            break
    # getting db info from current app
    my_db, my_cursor = flags.app.root.my_db, flags.app.root.my_cursor
    # retriving all students emails
    my_db.ping(reconnect=True)
    my_cursor.execute(f"select stud_email from students where pass_year = {year} and branch = {branch};")
    to = my_cursor.fetchall()
    # building mail message
    mail = EmailMessage()
    mail['from'] = config('email')
    mail['subject'] = subject
    mail.set_content(message)
    error_list=[]
    error_flag = False
    try:
        # logining to mail
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
            server.login(config('email'),config('email_password'))
            # list all mail address where mail couldnt be sent
            for i in to:
                try:
                    mail['to'] = i[0]
                    server.send_message(mail)
                except Exception:
                    error_flag = True
                    error_list.append(i[0])
                # show_alert_dialog(screen,"Mail sent to all students")
    # shows error messages
    except Exception:
        show_alert_dialog(screen,"Error sending mail to students")
    if error_flag:
        show_alert_dialog(screen,f"Error sending mail to {error_list}")
    # screen.wait_dialog.dismiss()
    
def get_close_matches_indexes(word, possibilities, n=3, cutoff=0.6):
    # get index of closest match of word from list of words
    # checking length
    if not n >  0:
        raise ValueError("n must be > 0: %r" % (n,))
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))
    result = []
    # using closest match value
    s = SequenceMatcher()
    s.set_seq2(word)
    for idx, x in enumerate(possibilities):
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and \
           s.quick_ratio() >= cutoff and \
           s.ratio() >= cutoff:
            result.append((s.ratio(), idx))

    # Move the best scorers to head of list
    result = _nlargest(n, result)

    # Strip scores for the best n matches
    return [x for score, x in result]
