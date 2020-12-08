import torch
from api.models.taco_models.forward_tacotron import ForwardTacotron
from api.models.utils.display import simple_table
from api.models.utils.dsp import reconstruct_waveform, save_wav
from api.models.utils.paths import Paths
from api.models.utils.text import clean_text, text_to_sequence
from api.models.utils.text.symbols import phonemes
import yaml
from munch import Munch
import os 


class GenForward:
    def __init__(self, input_text, model):
        self.vocoder = 'griffinlim'
        self.alpha = 1
        self.amp = 1
        self.max_iter = 32
        self.input_text = input_text
        self.data_path = 'data/'
        self.voc_model_id = f'{model}_raw' 
        self.tts_model_id = f'{model}_tts'
        self.paths = Paths(self.data_path, self.voc_model_id, self.tts_model_id)

    def generate_wav(self):
        if torch.cuda.is_available():
            device = torch.device('cuda')
        else:
            device = torch.device('cpu')

        print('Using device:', device)
        print('\nInitialising Forward TTS Model...\n')

        # Dir_path is dir of current file, used to localize taco_config
        dir_path = os.path.dirname(os.path.realpath(__file__))

        with open(rf'{dir_path}/taco_config.yaml') as f:
            loaded_yaml = yaml.safe_load(f)
            config = Munch(loaded_yaml)

        tts_model = ForwardTacotron(embed_dims=256,
                                    num_chars=len(phonemes),
                                    durpred_rnn_dims=64,
                                    durpred_conv_dims=256,
                                    durpred_dropout=config.durpred_dropout,
                                    pitch_rnn_dims=128,
                                    pitch_conv_dims=256,
                                    pitch_dropout=config.pitch_dropout,
                                    pitch_emb_dims=64,
                                    pitch_proj_dropout=config.pitch_proj_dropout,
                                    rnn_dim=512,
                                    postnet_k=8,
                                    postnet_dims=256,
                                    prenet_k=16,
                                    prenet_dims=256,
                                    highways=config.highways,
                                    dropout=config.dropout,
                                    n_mels=80).to(device)
        tts_weights = None
        tts_load_path = tts_weights if tts_weights else self.paths.forward_latest_weights
        tts_model.load(tts_load_path)

        text = clean_text(self.input_text.strip())
        inputs = [text_to_sequence(text)]

        tts_k = tts_model.get_step() // 1000

        simple_table([('Forward Tacotron', str(tts_k) + 'k'),
                      ('Vocoder Type', 'Griffin-Lim'),
                      ('GL Iters', self.max_iter)])

        # simple amplification of pitch
        pitch_function = lambda x: x * self.amp

        for i, x in enumerate(inputs, self.alpha):

            print(f'\n| Generating {i}/{len(inputs)}')
            _, m, dur, pitch = tts_model.generate(x, alpha=self.alpha, pitch_function=pitch_function)

            v_type = self.vocoder

            if self.input_text:
                save_path = self.paths.forward_output / f'{self.input_text[:10]}_{self.alpha}_{v_type}_{tts_k}k_amp{self.amp}.wav'
            else:
                save_path = self.paths.forward_output / f'{i}_{v_type}_{tts_k}k_alpha{self.alpha}_amp{self.amp}.wav'

            wav = reconstruct_waveform(m, n_iter=self.max_iter)
            save_wav(wav, save_path)

        return save_path
