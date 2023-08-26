from src.View.BaseView import *
from src.ViewControl.ChildrenCtrl.ExcelGenerator import *


class ExcelGeneratorView(BaseView):
    def __reviewBtn_clicked(self):
        excel_path = tkinter.filedialog.asksaveasfilename(
            filetypes=[("Excel file", ".xlsx")]
            )
        self.path_entry.delete(0, tkinter.END)
        self.path_entry.insert(0, excel_path + ".xlsx")

    def __excel_btn_clicked(self):
        nameTable = self.combobox.get()
        pathExcel = self.path_entry.get()
        if self.sheet_entry.get() == '':
            name_page = 'Sheet'
        else:
            name_page = self.sheet_entry.get()
        self.excelGenerator.create_excel_table(nameTable, pathExcel, name_page)

    def __create_and_pack_elements(self):
        path_label = tkinter.Label(self.left_frame, text="Путь сохранения", font=self.heading_font, bg=self.leftBG)
        path_label.pack(pady=5, fill="x")
        self.path_entry = tkinter.Entry(self.left_frame)
        self.path_entry.pack(fill='x', padx=5, pady=5)
        review_btn = tkinter.Button(self.left_frame, text="Обзор", command=self.__reviewBtn_clicked)
        review_btn.pack(fill="x", padx=5, pady=5)
        name_page_label = tkinter.Label(self.left_frame, text="Название страницы", font=self.heading_font, bg=self.leftBG)
        name_page_label.pack(pady=5, fill="x")
        self.sheet_entry = tkinter.Entry(self.left_frame)
        self.sheet_entry.pack(fill='x', padx=5, pady=5)
        
        name_table_label = tkinter.Label(self.right_frame, text="Название таблицы", font=self.heading_font)
        name_table_label.pack(pady=5, fill="x")
        self.combobox = tkinter.ttk.Combobox(self.right_frame, values=self.excelGenerator.set_tables_combobox(),
                                              postcommand=lambda: self.combobox.configure(values=self.excelGenerator.set_tables_combobox()))
        self.combobox.pack(pady=5, fill="x", padx=5)
        action_table_btn = tkinter.Button(self.right_frame, text="Создать таблицу Excel", command=self.__excel_btn_clicked)
        action_table_btn.pack(fill='x', pady=5, padx=5)

        buttons_frame = tkinter.Frame(self.right_frame)
        buttons_frame.place(y=110, relx=0.01, relwidth=0.98, height=30)
        show_tables_btn = tkinter.Button(buttons_frame, text="Вывести все таблицы", command=self.excelGenerator.show_tables)
        show_tables_btn.place(relx=0, rely=0, relheight=1, relwidth=0.49)
        clear_console_btn = tkinter.Button(buttons_frame, text="Очистить консоль", command=self.excelGenerator.clear_console)
        clear_console_btn.place(relx=0.51, rely=0, relheight=1, relwidth=0.49)

    def __init__(self):
        super().__init__()
        self.excelGenerator = ExcelGenerator(self.console)
        self.__create_and_pack_elements()