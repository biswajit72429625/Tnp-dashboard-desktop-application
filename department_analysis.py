from kivy.uix.screenmanager import Screen


class DepartmentAnalysis(Screen):
    def __init__(self, **kw):
        super(DepartmentAnalysis,self).__init__(**kw)

    def function_called(self):
        print(self.ids)