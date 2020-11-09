import math
import struct

import torch
import numpy as np
import librosa
import webrtcvad
from scipy.ndimage import binary_dilation

from utils import hparams as hp
from scipy.signal import lfilter


def label_2_float(x, bits):
    return 2 * x / (2**bits - 1.) - 1.


def float_2_label(x, bits):
    assert abs(x).max() <= 1.0
    x = (x + 1.) * (2**bits - 1) / 2
    return x.clip(0, 2**bits - 1)


def load_wav(path):
    return librosa.load(path, sr=hp.sample_rate)[0]


def save_wav(x, path):
    librosa.output.write_wav(path, x.astype(np.float32), sr=hp.sample_rate)


def split_signal(x):
    unsigned = x + 2**15
    coarse = unsigned // 256
    fine = unsigned % 256
    return coarse, fine


def combine_signal(coarse, fine):
    return coarse * 256 + fine - 2**15


def encode_16bits(x):
    return np.clip(x * 2**15, -2**15, 2**15 - 1).astype(np.int16)


def linear_to_mel(spectrogram):
    return librosa.feature.melspectrogram(
        S=spectrogram, sr=hp.sample_rate, n_fft=hp.n_fft, n_mels=hp.num_mels, fmin=hp.fmin, fmax=hp.fmax)

'''
def build_mel_basis():
    return librosa.filters.mel(hp.sample_rate, hp.n_fft, n_mels=hp.num_mels, fmin=hp.fmin)
'''


def normalize(S):
    S = np.clip(S, a_min=1.e-5, a_max=None)
    return np.log(S)


def denormalize(S):
    return np.exp(S)


def melspectrogram(y):
    D = stft(y)
    S = linear_to_mel(np.abs(D))
    return normalize(S)

def raw_melspec(y):
    D = stft(y)
    S = linear_to_mel(np.abs(D))
    return S



def stft(y):
    return librosa.stft(
        y=y,
        n_fft=hp.n_fft, hop_length=hp.hop_length, win_length=hp.win_length)


def pre_emphasis(x):
    return lfilter([1, -hp.preemphasis], [1], x)


def de_emphasis(x):
    return lfilter([1], [1, -hp.preemphasis], x)


def encode_mu_law(x, mu):
    mu = mu - 1
    fx = np.sign(x) * np.log(1 + mu * np.abs(x)) / np.log(1 + mu)
    return np.floor((fx + 1) / 2 * mu + 0.5)


def decode_mu_law(y, mu, from_labels=True):
    # TODO: get rid of log2 - makes no sense
    if from_labels: y = label_2_float(y, math.log2(mu))
    mu = mu - 1
    x = np.sign(y) / mu * ((1 + mu) ** np.abs(y) - 1)
    return x


def np_now(x: torch.Tensor): return x.detach().cpu().numpy()


def trim_silence(wav):
    return librosa.effects.trim(wav, top_db=hp.trim_silence_top_db, frame_length=2048, hop_length=512)[0]


# from https://github.com/resemble-ai/Resemblyzer/blob/master/resemblyzer/audio.py
def trim_long_silences(wav):
    int16_max = (2 ** 15) - 1
    samples_per_window = (hp.vad_window_length * hp.vad_sample_rate) // 1000
    wav = wav[:len(wav) - (len(wav) % samples_per_window)]
    pcm_wave = struct.pack("%dh" % len(wav), *(np.round(wav * int16_max)).astype(np.int16))
    voice_flags = []
    vad = webrtcvad.Vad(mode=3)
    for window_start in range(0, len(wav), samples_per_window):
        window_end = window_start + samples_per_window
        voice_flags.append(vad.is_speech(pcm_wave[window_start * 2:window_end * 2],
                                         sample_rate=hp.vad_sample_rate))
    voice_flags = np.array(voice_flags)
    def moving_average(array, width):
        array_padded = np.concatenate((np.zeros((width - 1) // 2), array, np.zeros(width // 2)))
        ret = np.cumsum(array_padded, dtype=float)
        ret[width:] = ret[width:] - ret[:-width]
        return ret[width - 1:] / width
    audio_mask = moving_average(voice_flags, hp.vad_moving_average_width)
    audio_mask = np.round(audio_mask).astype(np.bool)
    audio_mask[:] = binary_dilation(audio_mask[:], np.ones(hp.vad_max_silence_length + 1))
    audio_mask = np.repeat(audio_mask, samples_per_window)
    return wav[audio_mask]


def reconstruct_waveform(mel, n_iter=32):
    """Uses Griffin-Lim phase reconstruction to convert from a normalized
    mel spectrogram back into a waveform."""
    denormalized = denormalize(mel)
    S = librosa.feature.inverse.mel_to_stft(
        denormalized, power=1, sr=hp.sample_rate,
        n_fft=hp.n_fft, fmin=hp.fmin, fmax=hp.fmax)
    wav = librosa.core.griffinlim(
        S, n_iter=n_iter,
        hop_length=hp.hop_length, win_length=hp.win_length)
    return wav

