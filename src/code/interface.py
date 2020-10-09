import sounddevice as sd
import config 

from tkinter import *
from stt import SpeechToText
from tts import textToSpeech
from audio_player import AudioPlayer


class Interface:
    gui = None
    selected_input_device = None
    selected_output_device = None
    stt = None
    tts = None
    ap = None

    def __init__(self, windowsize = config.default_window_size):
        self.gui = Tk(className = config.application_name)
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
            self.stt.record_and_save_wav()
            self.tts.create_wav()
            self.ap.play_wav()
        
        # get data for gui
        current_input_device, current_output_device, input_device, output_device = self._possible_device()

        # create input dropdown
        inp, inp_drop = self._create_dropdown(current_input_device, input_device)
        inp_drop.pack()

        # create input confirm
        confrm = self._create_button("Input Device",confirm_input)
        confrm.pack()

        # create output dropdown
        outp, outp_drop = self._create_dropdown(current_output_device, output_device)
        outp_drop.pack()

        # create output confirm
        confrm =  self._create_button("Output Device",confirm_output)
        confrm.pack()    

        # create recording button
        rec = self._create_button("Record",record)
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

    def _create_dropdown(self, current, options):
        var = StringVar(self.gui)
        var.set(current)
        drop = OptionMenu(self.gui, var, *options)
        drop.config(width=config.default_dropdown_width)
        return var, drop

    def _create_button(self, text, command):
        return Button(self.gui, text=text, command=command, width=config.default_btn_width, height=config.default_btn_height)

i = Interface()
i.start()