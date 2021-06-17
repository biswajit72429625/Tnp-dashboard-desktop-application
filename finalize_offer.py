from kivy.uix.screenmanager import Screen
from kivymd.uix.filemanager import MDFileManager

class FinalizeOffer(Screen):
    def __init__(self, **kw):
        super(FinalizeOffer, self).__init__(**kw)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager = self.exit_manager,
            select_path = self.select_path,
            # preview = True
            ext=[".xlsx",".csv",".txt",".xls"]
        )

    def file_manager_open(self):
        self.file_manager.show('C:/Users')
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        print(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()