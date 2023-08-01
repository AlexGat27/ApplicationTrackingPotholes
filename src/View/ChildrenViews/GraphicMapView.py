from src.View.BaseView import *
from src.ViewControl.ChildrenCtrl.GraphicalMapGenerator import *

class GraphicMapView(BaseView):
    
    def __create_and_pack_elements(self):
        super().create_and_pack_elements()

    def __init__(self):
        super().__init__()
        self.__create_and_pack_elements()
        self.graphMapGenerator = GraphicalMapGenerator()