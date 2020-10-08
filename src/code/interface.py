import sounddevice as sd

from tkinter import *
from stt import SpeechToText
from tts import textToSpeech
from audio_player import AudioPlayer
from config import default_window_size, application_name, default_btn_width, default_btn_height, default_dropdown_width

class Interface:
    gui = None
    selected_input_device = None
    selected_output_device = None
    stt = None
    tts = None
    ap = None

    def __init__(self, windowsize = default_window_size):
        self.gui = Tk(className = application_name)
        self.gui.geometry(windowsize)
        self.stt = SpeechToText()
        self.tts = textToSpeech()
        self.ap = AudioPlayer()

    def start(self):
        def confirm_input():
            self._set_input_device(int(inp.get().replace('{','').replace('}','')[0]))

        def confirm_output():
            self._set_output_device(int(outp.get().replace('{','').replace('}','')[0]))
        
        def record():
            self.stt.record_and_classify()
            self.tts.create_wav()
            self.ap.play_wav()
        
        # get data for gui
        current_input_device, current_output_device, input_device, output_device = self._possible_device()

        # create input dropdown
        inp = StringVar(self.gui)
        inp.set(current_input_device)
        inp_drop = OptionMenu(self.gui, inp, *input_device)
        inp_drop.config(width=default_dropdown_width)
        inp_drop.pack()

        # create input confirm
        confrm = Button(self.gui, text="Input Device", command=confirm_input, width=default_btn_width, height=default_btn_height)
        confrm.pack()

        # create output dropdown
        outp = StringVar(self.gui)
        outp.set(current_output_device)
        outp_drop = OptionMenu(self.gui, outp, *output_device)
        outp_drop.config(width=default_dropdown_width)
        outp_drop.pack()

        # create output confirm
        confrm = Button(self.gui, text="Output Device", command=confirm_output, width=default_btn_width, height=default_btn_height)
        confrm.pack()    

        # create recording button
        rec = Button(self.gui, text="Record", command=record, width=default_btn_width, height=default_btn_height)
        rec.pack()

        mainloop() 
    
    def _possible_device(self):
        devices = sd.query_devices()
        input_device, output_device = sd.default.device
        i = [{i: devices[i]['name']} for i in range(len(devices)) if devices[i]['max_input_channels'] > 0]
        o = [{i: devices[i]['name']} for i in range(len(devices)) if devices[i]['max_output_channels'] > 0]     

        self.selected_input_device = input_device
        self.selected_output_device = output_device
        return  {input_device: devices[input_device]['name']}, {output_device: devices[output_device]['name']}, i, o
        
    def _set_input_device(self, i_d):
        self.selected_input_device = i_d
        print(f'new input: {i_d}, new output: {self.selected_output_device}')
        sd.default.device = i_d, self.selected_output_device
        
    def _set_output_device(self, o_d):
        self.selected_output_device = o_d
        print(f'new input: {self.selected_input_device}, new output: {o_d}')
        sd.default.device = self.selected_input_device, o_d

i = Interface()
i.start()
