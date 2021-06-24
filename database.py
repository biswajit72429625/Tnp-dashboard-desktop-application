import mysql.connector as MYSQL
from decouple import config
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from functools import partial
from email.message import EmailMessage
import smtplib
from decouple import config
from difflib import SequenceMatcher
from heapq import nlargest as _nlargest

def db_connector():
    # connects to database
    #my_db = MYSQL.connect(host='remotemysql.com',username='PKuyMx1oEg',passwd='DopOx9wsho',database='PKuyMx1oEg', port=3306)
    my_db = MYSQL.connect(host='localhost',username=config('user'),passwd=config('passwd'),database='wit_tnp')
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

def send_mail(screen,subject:str,message:str,to:list):
    mail = EmailMessage()
    mail['from'] = config('email')
    mail['subject'] = subject
    mail.set_content(message)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
            server.login(config('email'),config('email_password'))
            for i in to:
                mail['to'] = i
                server.send_message(mail)
                # show_alert_dialog(screen,"Mail sent to all students")
    except Exception:
        show_alert_dialog(screen,"Error sending mail to students")
    
def get_close_matches_indexes(word, possibilities, n=3, cutoff=0.6):
    """Use SequenceMatcher to return a list of the indexes of the best 
    "good enough" matches. word is a sequence for which close matches 
    are desired (typically a string).
    possibilities is a list of sequences against which to match word
    (typically a list of strings).
    Optional arg n (default 3) is the maximum number of close matches to
    return.  n must be > 0.
    Optional arg cutoff (default 0.6) is a float in [0, 1].  Possibilities
    that don't score at least that similar to word are ignored.
    """

    if not n >  0:
        raise ValueError("n must be > 0: %r" % (n,))
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))
    result = []
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