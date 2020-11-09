from pathlib import Path
from typing import Union, Callable, List

import numpy as np

import torch.nn as nn
import torch
import torch.nn.functional as F

from models.tacotron import CBHG


class LengthRegulator(nn.Module):

    def __init__(self):
        super().__init__()

    def forward(self, x, dur):
        return self.expand(x, dur)

    @staticmethod
    def build_index(duration, x):
        duration[duration < 0] = 0
        tot_duration = duration.cumsum(1).detach().cpu().numpy().astype('int')
        max_duration = int(tot_duration.max().item())
        index = np.zeros([x.shape[0], max_duration, x.shape[2]], dtype='long')

        for i in range(tot_duration.shape[0]):
            pos = 0
            for j in range(tot_duration.shape[1]):
                pos1 = tot_duration[i, j]
                index[i, pos:pos1, :] = j
                pos = pos1
            index[i, pos:, :] = j
        return torch.LongTensor(index).to(duration.device)

    def expand(self, x, dur):
        idx = self.build_index(dur, x)
        y = torch.gather(x, 1, idx)
        return y


class SeriesPredictor(nn.Module):

    def __init__(self, in_dims, conv_dims=256, rnn_dims=64, dropout=0.5):
        super().__init__()
        self.convs = torch.nn.ModuleList([
            BatchNormConv(in_dims, conv_dims, 5, activation=torch.relu),
            BatchNormConv(conv_dims, conv_dims, 5, activation=torch.relu),
            BatchNormConv(conv_dims, conv_dims, 5, activation=torch.relu),
        ])
        self.rnn = nn.GRU(conv_dims, rnn_dims, batch_first=True, bidirectional=True)
        self.lin = nn.Linear(2 * rnn_dims, 1)
        self.dropout = dropout

    def forward(self, x, alpha=1.0):
        x = x.transpose(1, 2)
        for conv in self.convs:
            x = conv(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        x = x.transpose(1, 2)
        x, _ = self.rnn(x)
        x = self.lin(x)
        return x / alpha


class ConvResNet(nn.Module):

    def __init__(self, in_dims, conv_dims=256):
        super().__init__()
        self.first_conv = BatchNormConv(in_dims, conv_dims, 5, activation=torch.relu)
        self.convs = torch.nn.ModuleList([
            BatchNormConv(conv_dims, conv_dims, 5, activation=torch.relu),
            BatchNormConv(conv_dims, conv_dims, 5, activation=torch.relu),
        ])

    def forward(self, x):
        x = x.transpose(1, 2)
        x = self.first_conv(x)
        for conv in self.convs:
            x_res = x
            x = conv(x)
            x = x_res + x
        x = x.transpose(1, 2)
        return x

class BatchNormConv(nn.Module):

    def __init__(self, in_channels, out_channels, kernel, activation=None):
        super().__init__()
        self.conv = nn.Conv1d(in_channels, out_channels, kernel, stride=1, padding=kernel // 2, bias=False)
        self.bnorm = nn.BatchNorm1d(out_channels)
        self.activation = activation

    def forward(self, x):
        x = self.conv(x)
        if self.activation:
            x = self.activation(x)
        x = self.bnorm(x)
        return x


class ForwardTacotron(nn.Module):

    def __init__(self,
                 embed_dims,
                 num_chars,
                 durpred_conv_dims,
                 durpred_rnn_dims,
                 durpred_dropout,
                 pitch_conv_dims,
                 pitch_rnn_dims,
                 pitch_dropout,
                 pitch_emb_dims,
                 pitch_proj_dropout,
                 rnn_dim,
                 prenet_k,
                 prenet_dims,
                 postnet_k,
                 postnet_dims,
                 highways,
                 dropout,
                 n_mels):
        super().__init__()
        self.rnn_dim = rnn_dim
        self.embedding = nn.Embedding(num_chars, embed_dims)
        self.lr = LengthRegulator()
        self.dur_pred = SeriesPredictor(embed_dims,
                                        conv_dims=durpred_conv_dims,
                                        rnn_dims=durpred_rnn_dims,
                                        dropout=durpred_dropout)
        self.pitch_pred = SeriesPredictor(embed_dims,
                                          conv_dims=pitch_conv_dims,
                                          rnn_dims=pitch_rnn_dims,
                                          dropout=pitch_dropout)
        self.prenet = CBHG(K=prenet_k,
                           in_channels=embed_dims,
                           channels=prenet_dims,
                           proj_channels=[prenet_dims, embed_dims],
                           num_highways=highways)
        self.lstm = nn.LSTM(2 * prenet_dims + pitch_emb_dims,
                            rnn_dim,
                            batch_first=True,
                            bidirectional=True)
        self.lin = torch.nn.Linear(2 * rnn_dim, n_mels)
        self.register_buffer('step', torch.zeros(1, dtype=torch.long))
        self.postnet = CBHG(K=postnet_k,
                            in_channels=n_mels,
                            channels=postnet_dims,
                            proj_channels=[postnet_dims, n_mels],
                            num_highways=highways)
        self.dropout = dropout
        self.post_proj = nn.Linear(2 * postnet_dims, n_mels, bias=False)
        self.pitch_emb_dims = pitch_emb_dims
        if pitch_emb_dims > 0:
            self.pitch_proj = nn.Sequential(
                nn.Conv1d(1, pitch_emb_dims, kernel_size=3, padding=1),
                nn.Dropout(pitch_proj_dropout))

    def forward(self, x, mel, dur, mel_lens, pitch):
        if self.training:
            self.step += 1

        x = self.embedding(x)
        dur_hat = self.dur_pred(x).squeeze()
        pitch_hat = self.pitch_pred(x).transpose(1, 2)
        pitch = pitch.unsqueeze(1)

        x = x.transpose(1, 2)
        x = self.prenet(x)

        if self.pitch_emb_dims > 0:
            pitch_proj = self.pitch_proj(pitch)
            pitch_proj = pitch_proj.transpose(1, 2)
            x = torch.cat([x, pitch_proj], dim=-1)

        x = self.lr(x, dur)
        for i in range(x.size(0)):
            x[i, mel_lens[i]:, :] = 0

        x, _ = self.lstm(x)

        x = F.dropout(x,
                      p=self.dropout,
                      training=self.training)
        x = self.lin(x)
        x = x.transpose(1, 2)

        x_post = self.postnet(x)
        x_post = self.post_proj(x_post)
        x_post = x_post.transpose(1, 2)

        x_post = self.pad(x_post, mel.size(2))
        x = self.pad(x, mel.size(2))
        return x, x_post, dur_hat, pitch_hat

    def generate(self,
                 x: List[int],
                 alpha=1.0,
                 pitch_function: Callable[[torch.tensor], torch.tensor] = lambda x: x) -> tuple:
        self.eval()
        device = next(self.parameters()).device  # use same device as parameters
        x = torch.as_tensor(x, dtype=torch.long, device=device).unsqueeze(0)

        x = self.embedding(x)
        dur = self.dur_pred(x, alpha=alpha)
        dur = dur.squeeze(2)

        pitch_hat = self.pitch_pred(x).transpose(1, 2)
        pitch_hat = pitch_function(pitch_hat)

        x = x.transpose(1, 2)
        x = self.prenet(x)

        if self.pitch_emb_dims > 0:
            pitch_hat_proj = self.pitch_proj(pitch_hat).transpose(1, 2)
            x = torch.cat([x, pitch_hat_proj], dim=-1)

        x = self.lr(x, dur)

        x, _ = self.lstm(x)
        x = F.dropout(x,
                      p=self.dropout,
                      training=self.training)
        x = self.lin(x)
        x = x.transpose(1, 2)

        x_post = self.postnet(x)
        x_post = self.post_proj(x_post)
        x_post = x_post.transpose(1, 2)

        x, x_post, dur = x.squeeze(), x_post.squeeze(), dur.squeeze()
        x = x.cpu().data.numpy()
        x_post = x_post.cpu().data.numpy()
        dur = dur.cpu().data.numpy()

        return x, x_post, dur, pitch_hat

    def pad(self, x, max_len):
        x = x[:, :, :max_len]
        x = F.pad(x, [0, max_len - x.size(2), 0, 0], 'constant', -11.5129)
        return x

    def get_step(self):
        return self.step.data.item()

    def load(self, path: Union[str, Path]):
        # Use device of model params as location for loaded state
        device = next(self.parameters()).device
        state_dict = torch.load(path, map_location=device)
        self.load_state_dict(state_dict, strict=False)

    def save(self, path: Union[str, Path]):
        # No optimizer argument because saving a model should not include data
        # only relevant in the training process - it should only be properties
        # of the model itself. Let caller take care of saving optimzier state.
        torch.save(self.state_dict(), path)

    def log(self, path, msg):
        with open(path, 'a') as f:
            print(msg, file=f)

