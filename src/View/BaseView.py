import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.filedialog

class BaseView(tkinter.Frame):
    leftBG = '#E1E7E5'

    def create_and_pack_elements(self):
        self.left_frame = tkinter.Frame(self, bg=self.leftBG)
        self.left_frame.pack(side='left')
        self.left_frame.pack_propagate(False)
        self.left_frame.configure(width=200, height=470)
        self.right_frame = tkinter.Frame(self)
        self.right_frame.pack(side='left')
        self.right_frame.pack_propagate(False)
        self.right_frame.configure(width=500, height=470)

        self.console = tkinter.Text(self.right_frame)
        self.console.place(relx=0.01, y=150, relwidth=0.98, height=300)

    def packFrame(self):
        self.pack(padx=3, pady=3, fill='both')
        self.pack_propagate(False)
        self.configure(width=700, height=470)
    
    def __init__(self):
        super().__init__()
        self.config(bg="#F4FCFB", highlightthickness=1.5, highlightbackground="black")