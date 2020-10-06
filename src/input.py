from datetime import datetime

import sounddevice as sd
import soundfile as sf
import numpy as np

filename = 'recording_'+str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))+'.wav'
filelocation = f'./src/recordings/{filename}'

# get input and output devices
devices = sd.query_devices()
input_d, output_d = sd.default.device
input_device = devices[input_d]['name']
output_device = devices[output_d]['name']

print(f'devices: {devices}')
print(f'input: {input_device}, output: {output_device}')

# give user the possablity to change settings
while True:
    corr = input('Setting correct? (y/n)')
    if corr == 'y':
        break
    else:
        put = input('input or output? (i/o)')
        num = input('correct number?')
        if put == 'i':
            input_d = int(num)
        elif put == 'o':
            output_d = int(num)
        else:
            print('incorrect try again') 

# set new output and input devices
print(output_d, input_d, type(output_d), type(input_d))
sd.default.device = input_d, output_d

# recording
fs = 44100
second = 10
print('recording...')
record_voice = sd.rec(int(second * fs),samplerate=fs,channels=2)
sd.wait()
sf.write(filelocation, record_voice, fs)
print('finnished')