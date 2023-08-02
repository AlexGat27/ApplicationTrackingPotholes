from src.View.BaseView import *
from src.ViewControl.ChildrenCtrl.CheckDatabaseProcess import *

class CheckDatabaseView(BaseView):
    def __create_and_pack_elements(self):
        pass

    def __init__(self):
        super().__init__()
        self.__create_and_pack_elements()
        self.__checkData = CheckDatabaseProcess()