from src.Controllers.BaseCtrl import *
import numpy as np
import pandas as pd

class ExcelGenerator(BaseCtrl):
    def __getCoordsFromPoint(self, point: str):
        point = point.replace('POINT', '')
        point = point.replace('(', '')
        point = point.replace(')', '')
        split_coords = point.split()
        return split_coords
    
    def __errorHandler(self, name, path):
        if not(self.checkConnectionBD()):
            return None
        if name == '':
            self.recordConsole("Не выбрано название таблицы\n\n")
            return None
        if path == '' or path.split('.')[-1] != 'xlsx':
            self.recordConsole("Неправильно выбран путь файла\n\n")
            return None

    def create_excel_table(self, name, path, sheet_name):
        if self.__errorHandler(name, path):
            return None
        
        info_db = self.database.getInfoFromTable(name)
        columns = np.array(["Crs3857_x", "Crs3857_y", "Crs4326_lat", "Crs4326_lon"])
        data_np = []
        for i, row in enumerate(info_db):
            new_row = self.__getCoordsFromPoint(row[0]) + self.__getCoordsFromPoint(row[1])
            if i == 0:
                data_np = new_row
            else:    
                data_np = np.vstack((data_np, new_row))

        data = pd.DataFrame(data=data_np, columns=columns)
        data.to_excel(path, sheet_name=sheet_name, index=False)
        self.recordConsole("Таблица {} в формате Excel успешно создана\n\n".format(name))