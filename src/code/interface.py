from tkinter import *
from stt import SpeechToText
from config import default_window_size

class Interface:
    gui = None
    def __init__(self, windowsize = default_window_size):
        self.gui = Tk(className='Elaine Voice')
        self.gui.geometry(windowsize)

    def start(self):
        def confirm():
            new_device = var.get().replace('{','').replace('}','')[0]
            stt.set_input_device(int(new_device))
        
        def record():
            stt.record_and_save_wav()
        
        stt = SpeechToText()
        current_device, device_list = stt.select_input_device()

        # create dropdown
        var = StringVar(self.gui)
        var.set(current_device)
        w = OptionMenu(self.gui, var, *device_list)
        w.pack()

        # create confirm dropdown
        confrm = Button(self.gui, text="Input Device", command=confirm)
        confrm.pack()  

        # create recording button
        rec = Button(self.gui, text="record", command=record)
        rec.pack()

        mainloop() 

i = Interface()
i.start()
