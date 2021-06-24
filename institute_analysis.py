from kivy.uix.screenmanager import Screen


class InstituteAnalysis(Screen):
    def __init__(self, **kw):
        super(InstituteAnalysis,self).__init__(**kw)

    def function_called(self):
        print(self.ids)