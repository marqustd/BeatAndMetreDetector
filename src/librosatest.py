# %%
import librosa
import numpy as np
import matplotlib.pyplot as plt

# %%
filename = librosa.ex("trumpet")
sample, sr = librosa.load(filename)
sample, sr

# %%
n_fft = 2048
win_length = n_fft
signal = librosa.stft(sample, n_fft=n_fft, win_length=win_length, hop_length=512)
signal

# %%
spectrogram = np.abs(signal) ** 2
spectrogram

# %%
frequencies = librosa.fft_frequencies(sr=22050, n_fft=n_fft)
frequencies

# %%
times = np.arange(0, len(sample) / sr, n_fft)
# %%
plt.pcolormesh(spectrogram, frequencies, cmap="magma")

# %%
