
#%% Load file
import librosa
signal, sr = librosa.load('song.wav')

#%% Calculate mfcc
mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=40)

#%% Visualize
import matplotlib.pyplot as plt
import librosa.display
fig, ax = plt.subplots()
img = librosa.display.specshow(mfccs, x_axis='time', ax=ax)
fig.colorbar(img, ax=ax)
ax.set(title='MFCC')

# %%
