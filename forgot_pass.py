from kivy.uix.screenmanager import Screen

class ForgotPass(Screen):
    def __init__(self, **kw):
        super(ForgotPass, self).__init__(**kw)
        self.ids.change.disabled = True
        self.ids.new_pass.disabled = True
        self.ids.confirm_pass.disabled = True