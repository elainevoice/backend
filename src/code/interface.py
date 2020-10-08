from tkinter import *
from stt import SpeechToText
from config import default_window_size, application_name, default_btn_width, default_btn_height, default_dropdown_width

class Interface:
    gui = None
    def __init__(self, windowsize = default_window_size):
        self.gui = Tk(className = application_name)
        self.gui.geometry(windowsize)

    def start(self):
        def confirm():
            stt.set_input_device(int(var.get().replace('{','').replace('}','')[0]))
        
        def record():
            stt.record_and_classify()
        
        stt = SpeechToText()
        current_device, device_list = stt.select_input_device()

        # create dropdown
        var = StringVar(self.gui)
        var.set(current_device)
        w = OptionMenu(self.gui, var, *device_list)
        w.config(width=default_dropdown_width)
        w.pack()

        # create confirm dropdown
        confrm = Button(self.gui, text="Input Device", command=confirm, width=default_btn_width, height=default_btn_height)
        confrm.pack()  

        # create recording button
        rec = Button(self.gui, text="record", command=record, width=default_btn_width, height=default_btn_height)
        rec.pack()

        mainloop() 

i = Interface()
i.start()
