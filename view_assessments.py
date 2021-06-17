from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.dialog import MDDialog

class AssessmentDialog(BoxLayout):
    pass

class ViewAssessments(Screen):
    dialog = None
    def __init__(self, **kw):
        super(ViewAssessments, self).__init__(**kw)
    
    def full_details(self,row_id):
        # shows all details of e_resource in a dialog box
        self.dialog = MDDialog(
            title=str(self.ids[f'{str(row_id)}'].text),
            type="custom",
            content_cls=AssessmentDialog(),
            buttons=[
                    MDRoundFlatButton(text="CANCEL",on_press=self.dismiss_dialog),
                    MDRoundFlatButton(text="SAVE"),
                ]
        )
        self.dialog.open()

    def dismiss_dialog(self,instance):
        self.dialog.dismiss()

    def add_delete(self,instance):
        if instance.icon == 'notebook-plus-outline':
            self.manager.current = 'add_assessments'
            self.manager.stack.append(self.name)
        else:
            pass