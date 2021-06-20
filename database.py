import mysql.connector as MYSQL
from decouple import config
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from functools import partial

def db_connector():
    # connects to database
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