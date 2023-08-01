from src.View.BaseView import *
from src.ViewControl.ChildrenCtrl.ExcelGenerator import *


class ExcelGeneratorView(BaseView):
    def __create_and_pack_elements(self):
        super().create_and_pack_elements()

    def __init__(self):
        super().__init__()
        self.__create_and_pack_elements()
        self.excelGenerator = ExcelGenerator()