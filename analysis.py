from kivy.uix.screenmanager import Screen


class Analysis(Screen):
    def __init__(self, **kw):
        super(Analysis, self).__init__(**kw)

    def load_individual(self):
        # loads analysis of individual student
        individual_screen = self.manager.get_screen("individual_level")
        individual_screen.load_table()


