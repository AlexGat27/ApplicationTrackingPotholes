from src.Controllers.BaseCtrl import *
import numpy as np
import pandas as pd

class ExcelGenerator(BaseCtrl):
    def _getCoordsFromPoint(self, info_np):
        coords = []
        for i, row in enumerate(info_np):
            row[3] = row[3].replace('POINT', '')
            row[3] = row[3].replace('(', '')
            row[3] = row[3].replace(')', '')
            split_coords = row[3].split()
            if i == 0:
                coords = split_coords
            else:
                coords = np.vstack((coords, split_coords))
        return coords

    def create_excel_table(self, name, path, sheet_name):
        if not(self.checkConnectionBD()):
            return None
        if name == '':
            self.recordConsole("Не выбрано название таблицы\n\n")
            return None
        if path == '' or path.split('.')[-1] != 'xlsx':
            self.recordConsole("Неправильно выбран путь файла\n\n")
            return None
        
        info_db = self.database.getInfoFromTable(name)
        columns = np.array(["Time_Add", "Time_detect", "crs3857_x", "crs3857_y", "crs4326_x", "crs4326_y"])
        info_np = []
        for i, row in enumerate(info_db):
            if i == 0:
                info_np = row
            else:    
                info_np = np.vstack((info_np, row))

        coords = self._getCoordsFromPoint(info_np)

        data = pd.DataFrame(data=np.hstack((info_np[:,:3], coords, info_np[:,4:5])), columns=columns)
        data.to_excel(path, sheet_name=sheet_name, index=False)
        self.recordConsole("Таблица {} в формате Excel успешно создана\n\n".format(name))