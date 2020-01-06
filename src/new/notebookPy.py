# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import numpy as np
import scipy.io.wavfile, scipy.signal
from matplotlib import pyplot as plt
import time

# %%
class Song:
    name = "name"
    bpm = 120,
    filepath = "test"

    def __init__(self, name, bpm, filepath):
        self.name = name
        self.bpm = bpm
        self.filepath = filepath
         


# %%
bandLimits = [0, 200, 400, 800, 1600, 3200, 6400]    
combFilterPulses = 8
minBpm = 60
maxBpm = 240

resampleSignal = True
resampleRatio = 4

drawPlots = True
drawFftPlots = True
drawCombFilterPlots = True
drawSongBpmEnergyPlot = True

useConvolveMethod = False

startTime = time.time()

song = Song("12-rotgut", 147, "songs\\rock\\12-rotgut.wav")


# %%
def prepare_plot_dictionary(minBpm, maxBpm):
    dictionary = {}
    for bpm in range(minBpm, maxBpm):
        dictionary[bpm] = 0
    return dictionary


# %%
def draw_plot(is_draw_plots:bool, yData, title, xAxis, yAxis, xData = 0):
    if is_draw_plots:
        if xData is 0:
            plt.plot(yData)
        else:
            plt.plot(yData, xData)
        plt.title(title)
        plt.xlabel(xAxis)
        plt.ylabel(yAxis)
        plt.show() 
        


# %%
def draw_fft_plot(drawPlots:bool, yData, plotTitle, samplingFrequency:int):
    if drawPlots:
        length = len(yData)
        h = abs(yData/length)
        h = h[1:int(length/2+1)]
        f = samplingFrequency * ((np.arange(0,int(length/2)))/length)
        
        plt.plot(f, h)
        plt.title(plotTitle)
        plt.xlabel("f[Hz]")
        plt.ylabel("|H(f)|")
        plt.xlim(0, 5000)
        plt.show()   


# %%
def draw_comb_filter_fft_plot(is_draw_plots:bool, yData, plotTitle, samplingFrequency:int):
    if is_draw_plots:
        length = len(yData)
        h = abs(yData/length)
        h = h[1:int(length/2+1)]
        f = samplingFrequency* ((np.arange(0,int(length/2)))/length)
        
        plt.plot(f, h)
        plt.title(plotTitle)
        plt.xlabel("f[Hz]")
        plt.ylabel("|H(f)|")
        plt.xlim(0, 10)
        plt.show() 


# %%
def center_sample_to_beat(signal, seconds):
    n = len(signal)
    index = 0

    max = np.max(abs(signal))

    for i in range(0, n):
        if abs(signal[i]) > max*0.9:
            index = i
            break

    lastindex = seconds
    lastindex += index
    if lastindex > n:
        lastindex = n
    return signal[index:int(lastindex)]


# %%
def prepare_filterbanks(signal, bandlimits, samplingFrequency):
    dft = np.fft.fft(signal)
    n = len(dft)
    nbands = len(bandlimits)
    bl = np.zeros(nbands, int)
    br = np.zeros(nbands, int)

    #   % Bring band scale from Hz to the points in our vectors
    for band in range(0, nbands - 1):
        bl[band] = np.floor(bandlimits[band] / samplingFrequency * n / 2) + 1
        br[band] = np.floor(bandlimits[band + 1] / samplingFrequency * n / 2)

    bl[0] = 0
    bl[nbands - 1] = np.floor(bandlimits[nbands - 1] / samplingFrequency * n / 2) + 1
    br[nbands - 1] = np.floor(n / 2)

    output = np.zeros([nbands, n], dtype=complex)

    # Create the frequency bands and put them in the vector output.
    for band in range(0, nbands):
        for hz in range(bl[band], br[band]):
            output[band, hz] = dft[hz]
        for hz in range(n - br[band], n - bl[band]):
            output[band, hz] = dft[hz]

    output[1, 1] = 0
    return output


# %%
def read_song(filename):
    sample_freq, data = scipy.io.wavfile.read(filename)
    signal = np.frombuffer(data, np.int16)
    return signal, sample_freq


# %%
def hann(signal, winLength, bandslimits, samplingFrequency):
    n = len(signal[0])
    nbands = len(bandslimits)
    hannlen = winLength * 2 * samplingFrequency
    hann = np.zeros(n)
    wave = np.zeros([nbands, n], dtype=complex)
    output = np.zeros([nbands, n], dtype=complex)
    freq = np.zeros([nbands, n], dtype=complex)
    filtered = np.zeros([nbands, n], dtype=complex)

    # Create half-Hanning window.
    for a in range(1, int(hannlen)):
        hann[a] = (np.cos(a * np.pi / hannlen / 2)) ** 2

    # Take IFFT to transfrom to time domain.
    for band in range(0, nbands):
        wave[band] = np.real(np.fft.ifft(signal[band]))

    # Full - wave rectification in the time domain. And back to frequency with FFT.
    for band in range(0, nbands):
        for j in range(0, n):
            if wave[band, j] < 0:
                wave[band, j] = -wave[band, j]
        freq[band] = np.fft.fft(wave[band])

    # Convolving with half - Hanning same as multiplying in frequency.Multiply half - Hanning
    # FFT by signal FFT.Inverse transform to get output in the time domain.
    for band in range(0, nbands):
        filtered[band] = freq[band] * np.fft.fft(hann)
        output[band] = np.real(np.fft.ifft(filtered[band]))

    return output


# %%
def diffrect(signal, nbands=6):
    n = len(signal[0])
    output = np.zeros([nbands, n], dtype=complex)

    for band in range(0, nbands):
        for j in range(5, n):
            d = signal[band, j] - signal[band, j-1]
            if d > 0:
                output[band, j] = d;

    return output


# %%
class CombFilterTempoDetector:    
    def detect_tempo(self, signal, accuracy:int, minBpm:int, maxBpm:int, bandsLimits, samplingFrequency, combFilterPulses, plotDictionary):
        n = len(signal[0])
        bands_amount = len(bandsLimits)
        dft = np.zeros([bands_amount, n], dtype=complex)
    
        if minBpm < 60:
            minBpm = 60
    
        if maxBpm > 240:
            maxBpm = 240
    
        # Get signal in frequency domain
        for band in range(0, bands_amount):
            dft[band] = np.fft.fft(signal[band])
            draw_fft_plot(drawFftPlots, dft[band], f"Band[{band}] DFT", samplingFrequency)
    
        # % Initialize max energy to zero
        maxEnergy = 0
        for bpm in range(minBpm, maxBpm, accuracy):
            # % Initialize energy and filter to zero(s)
            this_bpm_energy = 0
            fil = np.zeros(n)
    
            # Calculate the difference between peaks in the filter for a certain tempo
            filter_step = np.floor(60 / bpm * samplingFrequency)
            percent_done = 100 * (bpm - minBpm) / (maxBpm - minBpm)
            print(percent_done)
    
    
            # Set every filter's step samples of the filter to one
            for a in range(0, combFilterPulses):
                fil[a * int(filter_step) + 1] = 1
    
            draw_plot(drawCombFilterPlots, fil, f"Timecomb bpm: {bpm}", "Sample/Time", "Amplitude")
            # Get the filter in the frequency domain
            dftfil = np.fft.fft(fil)
            draw_comb_filter_fft_plot(drawFftPlots, dftfil, f"Filter's signal DFT {bpm}", samplingFrequency)
    
            for band in range(0, bands_amount):
                x = (abs(dftfil * dft[band])) ** 2
                this_bpm_energy = this_bpm_energy + sum(x)
    
            plotDictionary[bpm] = this_bpm_energy
            # If greater than all previous energies, set current bpm to the bpm of the signal
            if this_bpm_energy > maxEnergy:
                songBpm = bpm
                maxEnergy = this_bpm_energy
    
        return songBpm


# %%
class ConvolveTempoDetector:
    def detect_tempo(self, signal, accuracy:int, minBpm:int, maxBpm:int, bandsLimits, samplingFrequency, combFilterPulses, plotDictionary):
        n = len(signal[0])
        nbands = len(bandsLimits)
        dft = np.zeros([nbands, n], dtype=complex)
    
        if minBpm < 60:
            minBpm = 60
    
        if maxBpm > 240:
            maxBpm = 240
    
        # Get signal in frequency domain
        for band in range(0, nbands):
            dft[band] = np.fft.fft(signal[band])
            draw_fft_plot(drawFftPlots, dft[band], f"Band[{band}] DFT", samplingFrequency)
    
        # % Initialize max energy to zero
        maxe = 0
        for bpm in range(minBpm, maxBpm, accuracy):
            # % Initialize energy and filter to zero(s)
            e = 0
    
            # Calculate the difference between peaks in the filter for a certain tempo
            filterLength = 2
            nstep = np.floor(60 / bpm * samplingFrequency)
            percent_done = 100 * (bpm - minBpm) / (maxBpm - minBpm)
            fil = np.zeros(int(filterLength * nstep))
    
            print(percent_done)
    
            # Set every nstep samples of the filter to one
            for a in range(0, filterLength):
                fil[a * int(nstep)] = 1
    
            draw_plot(drawCombFilterPlots, fil, f"Timecomb bpm: {bpm}", "Sample/Time", "Amplitude")
    
            # Get the filter in the frequency domain
            dftfil = np.fft.fft(fil)
            # dftfil = scipy.signal.resample(dftfil, len(dft[0]))
    
            draw_comb_filter_fft_plot(drawCombFilterPlots, dftfil, f"Filter DFT {bpm}", samplingFrequency)
            for band in range(0, nbands-1):
                filt = scipy.convolve(signal[band], fil)
                f_filt = abs(np.fft.fft(filt))
                draw_fft_plot(drawFftPlots, f_filt, f"Convolve DFT {bpm}", samplingFrequency)
    
                x = abs(f_filt)**2
                e = e + sum(x)
    
    
            plotDictionary[bpm] = e
            # If greater than all previous energies, set current bpm to the bpm of the signal
            if e > maxe:
                sbpm = bpm
                maxe = e
    
        return sbpm


# %%
class DetectMetre:
    def detect_metre(self, signal, songTempo: int, bandlimits, samplingFrequency, combFilterPulses):
        length = len(signal[0])
        print(length)
        n = int(combFilterPulses * samplingFrequency * (60 / songTempo))
        print(n)
        nbands = len(bandlimits)
        dft = np.zeros([nbands, n], dtype=complex)

        # Get signal in frequency domain
        for band in range(0, nbands):
            dft[band] = np.fft.fft(signal[band, 0:n])
            draw_plot(drawPlots, signal[band], f"Signal[{band}]", "Sample/Time", "Amplitude")
            draw_fft_plot(drawFftPlots, dft[band], f"Signal[{band}] dft", samplingFrequency)
            draw_comb_filter_fft_plot(drawFftPlots, dft[band], f"Signal[{band}] dft", samplingFrequency)

        metres = {}
        metre, metre_dft = self.__four_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__three_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__five_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__six_eigth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        # % Initialize max energy to zero
        maxe = 0
        for metrum in metres:
            # % Initialize energy and filter to zero(s)
            e = 0

            for band in range(0, nbands):
                x = (abs(metres[metrum] * dft[band])) ** 2
                e = e + sum(x)

            # If greater than all previous energies, set current bpm to the bpm of the signal
            if e > maxe:
                song_metre = metrum
                maxe = e

        return song_metre

    def __four_forth(self, songTempo, n, samplingFrequency, combFilterPulses):
        fil = np.zeros(n)
        nstep = np.floor(60 / songTempo * samplingFrequency)
        index = 0
        bit = 0
        while index < n and bit <= combFilterPulses:
            value = 1
            if bit % 2 > 0:
                value = 0

            fil[int(index)] = value
            index += nstep
            bit += 1

        draw_plot(drawCombFilterPlots, fil, "4/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 4/4 filter dft", samplingFrequency)
        energy = sum(abs(dft) ** 2)
        print("filter 4/4 energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("normalized filter 4/4 energy: ", energy)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 4/4 filter normalized dft", samplingFrequency)
        return "4/4", dft

    def __three_forth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(n)
        nstep = np.floor(60 / songTempo * samplingFrequency)  # every third bit
        index = 0
        bit = 0
        while index < n and bit <= filter_pulses:
            value = 1
            if bit % 3 > 0:
                value = 0
            fil[int(index)] = value
            index += nstep
            bit += 1

        draw_plot(drawCombFilterPlots, fil, "3/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 3/4 filter dft", samplingFrequency)
        energy = sum(abs(dft) ** 2)
        print("filter 3/4 energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("normalized filter 3/4 energy: ", energy)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 3/4 filter normalized dft", samplingFrequency)
        return "3/4", dft

    def __five_forth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(n)
        nstep = np.floor(60 / songTempo * samplingFrequency)  # every third bit
        index = 0
        bits = 0
        bit = 1
        while index < n and bits <= filter_pulses:
            value = 0
            if bit == 2 or bit == 4 or bit == 5:
                value = 1
            fil[int(index)] = value
            index += nstep
            bit += 1
            bits += 1
            if bit > 5:
                bit = 1

        draw_plot(drawCombFilterPlots, fil, "5/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 5/4 filter dft", samplingFrequency)
        energy = sum(abs(dft) ** 2)
        print("filter 5/4 energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("normalized filter 5/4 energy: ", energy)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 5/4 filter normalized dft", samplingFrequency)
        return "5/4", dft
    
    def __six_eigth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(n)
        nstep = np.floor((60 / songTempo * samplingFrequency)/2)
        bit = 0
        index = 0
        while index < n and bit <= filter_pulses*2:
            value = 1
            if bit % 3 > 0:
                value = 0
            fil[int(index)] = value
            index += nstep
            bit += 1

        draw_plot(drawCombFilterPlots, fil, "6/8", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 6/8 filter dft", samplingFrequency)
        energy = sum(abs(dft) ** 2)
        print("filter 6/8 energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("normalized filter 6/8 energy: ", energy)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 6/8 filter normalized dft", samplingFrequency)
        return "6/8", dft


# %%
class DetectMetreNormalized:
    def detect_metre(self, signal, songTempo: int, bandlimits, samplingFrequency, filter_pulses):
        length = len(signal[0])
        print(length)
        n = int(combFilterPulses * samplingFrequency * (60 / songTempo))
        print(n)
        nbands = len(bandlimits)
        dft = np.zeros([nbands, n], dtype=complex)

        # Get signal in frequency domain
        for band in range(0, nbands):
            dft[band] = np.fft.fft(signal[band, 0:n])
            draw_plot(drawPlots, signal[band], f"Signal[{band}]", "Sample/Time", "Amplitude")
            draw_fft_plot(drawFftPlots, dft[band], f"Signal[{band}] dft", samplingFrequency)
            draw_comb_filter_fft_plot(drawFftPlots, dft[band], f"Signal[{band}] dft", samplingFrequency)

        metres = {}
        metre, metre_dft = self.__four_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__three_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__five_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        # % Initialize max energy to zero
        maxe = 0
        for metrum in metres:
            # % Initialize energy and filter to zero(s)
            e = 0

            for band in range(0, nbands):
                x = (abs(metres[metrum] * dft[band])) ** 2
                e = e + sum(x)

            # If greater than all previous energies, set current bpm to the bpm of the signal
            if e > maxe:
                song_metre = metrum
                maxe = e

        return song_metre

    def __four_forth(self, songTempo, n, samplingFrequency, filter_pulses):
        fil = np.zeros(n)
        nstep = np.floor(60 / songTempo * samplingFrequency)
        index = 0
        bit = 0
        pulse = 1 / (filter_pulses + np.floor(filter_pulses / 2))
        while index < n and bit < filter_pulses:
            value = 2 * pulse
            if bit % 2 > 0:
                value = 1 * pulse

            fil[int(index)] = value
            index += nstep
            bit += 1

        filterSum = sum(abs(fil))
        print("Sum 4/4: ", filterSum)
        draw_plot(drawCombFilterPlots, fil, "4/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 4/4 filter dft", samplingFrequency)
        energy = sum(abs(dft) ** 2)
        print("filter 4/4 energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("normalized filter 4/4 energy: ", energy)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 4/4 filter normalized dft", samplingFrequency)
        return "4/4", dft

    def __three_forth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(n)
        nstep = np.floor(60 / songTempo * samplingFrequency)  # every third bit
        index = 0
        bit = 0

        pulse = 1 / (filter_pulses + np.floor(filter_pulses / 3))

        while index < n and bit < filter_pulses:
            value = 2 * pulse
            if bit % 3 > 0:
                value = 1 * pulse
            fil[int(index)] = value
            index += nstep
            bit += 1

        filterSum = sum(abs(fil))
        print("Sum 3/4: ", filterSum)
        draw_plot(drawCombFilterPlots, fil, "3/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 3/4 filter dft", samplingFrequency)
        energy = sum(abs(dft) ** 2)
        print("filter 3/4 energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("normalized filter 3/4 energy: ", energy)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 3/4 filter normalized dft", samplingFrequency)
        return "3/4", dft

    def __five_forth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(n)
        nstep = np.floor(60 / songTempo * samplingFrequency)  # every third bit
        index = 0
        bits = 0
        bit = 1

        pulse = 1 / (filter_pulses + np.floor(filter_pulses / 5) * 3 + abs(filter_pulses % 5 - 1))

        while index < n and bits < filter_pulses:
            value = 1 * pulse
            if bit == 2 or bit == 4 or bit == 5:
                value = 2 * pulse
            fil[int(index)] = value
            index += nstep
            bit += 1
            bits += 1
            if bit > 5:
                bit = 1

        filterSum = sum(abs(fil))
        print("Sum 5/4: ", filterSum)
        draw_plot(drawCombFilterPlots, fil, "5/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 5/4 filter dft", samplingFrequency)
        energy = sum(abs(dft) ** 2)
        print("filter 5/4 energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("normalized filter 5/4 energy: ", energy)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 5/4 filter normalized dft", samplingFrequency)
        return "5/4", dft


# %%
class DetectMetreConvolve:
    def detect_metre(self, signal, songTempo: int, bandlimits, samplingFrequency, combFilterPulses):
        length = len(signal[0])
        print(length)
        n = int(combFilterPulses * samplingFrequency * (60 / songTempo))
        print(n)
        nbands = len(bandlimits)

        for band in range(0, nbands):
            draw_plot(drawPlots, signal[band], f"band: {band}", "Sample/Time", "Amplitude")

        metres = {}
        metre, metre_dft = self.__four_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__three_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        #metre, metre_dft = self.__five_forth(songTempo, n, samplingFrequency, combFilterPulses)
        #metres[metre] = metre_dft
        metre, metre_dft = self.__six_eigth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        # % Initialize max energy to zero
        maxe = 0
        for metrum in metres:
            # % Initialize energy and filter to zero(s)
            e = 0

            for band in range(0, nbands):
                filt = scipy.convolve(signal[band], metres[metrum])
                f_filt = abs(np.fft.fft(filt))
                draw_plot(drawPlots, f_filt, metrum, "Sample/Time", "Amplitude")
                x = abs(f_filt) ** 2
                e = e + sum(x)

            # If greater than all previous energies, set current bpm to the bpm of the signal
            if e > maxe:
                song_metre = metrum
                maxe = e

        return song_metre

    def __four_forth(self, songTempo: int, n: int, samplingFrequency: int, combFilterPulses: int):
        fil = np.zeros(int(4 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor(60 / songTempo * samplingFrequency)

        value = 1
        fil[int(1 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value

        draw_plot(drawCombFilterPlots, fil, "4/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 4/4 filter dft", samplingFrequency)
        return "4/4", fil

    def __three_forth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(int(3 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor(60 / songTempo * samplingFrequency)

        value = 1
        fil[int(2 * nstep)] = 1 * value

        draw_plot(drawCombFilterPlots, fil, "3/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 3/4 filter dft", samplingFrequency)
        return "3/4", fil

    def __five_forth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(int(5 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor(60 / songTempo * samplingFrequency)

        value = 1
        fil[int(1 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value
        fil[int(4 * nstep)] = 1 * value

        draw_plot(drawCombFilterPlots, fil, "5/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 5/4 filter dft", samplingFrequency)
        return "5/4", fil
    
    def __six_eigth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(int(3 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor((60 / songTempo * samplingFrequency)/2)

        value = 1
        fil[int(0 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value

        draw_plot(drawCombFilterPlots, fil, "6/8", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 6/8 filter dft", samplingFrequency)
        return "6/8", fil


# %%
class DetectMetreConvolveNormalized:
    def detect_metre(self, signal, songTempo: int, bandlimits, samplingFrequency, combFilterPulses):
        length = len(signal[0])
        print(length)
        n = int(combFilterPulses * samplingFrequency * (60 / songTempo))
        print(n)
        nbands = len(bandlimits)

        for band in range(0, nbands):
            draw_plot(drawPlots, signal[band], f"band: {band}", "Sample/Time", "Amplitude")

        metres = {}
        metre, metre_dft = self.__four_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__three_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__five_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__six_eigth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        # % Initialize max energy to zero
        maxe = 0
        for metrum in metres:
            # % Initialize energy and filter to zero(s)
            e = 0

            for band in range(0, nbands):
                filt = scipy.convolve(signal[band], metres[metrum])
                f_filt = abs(np.fft.fft(filt))
                draw_plot(drawPlots, f_filt, metrum, "Sample/Time", "Amplitude")
                x = abs(f_filt) ** 2
                e = e + sum(x)

            # If greater than all previous energies, set current bpm to the bpm of the signal
            if e > maxe:
                song_metre = metrum
                maxe = e

        return song_metre

    def __four_forth(self, songTempo: int, n: int, samplingFrequency: int, combFilterPulses: int):
        fil = np.zeros(int(4 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor(60 / songTempo * samplingFrequency)

        value = 1 / 2
        fil[int(1 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value

        draw_plot(drawCombFilterPlots, fil, "4/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 4/4 filter dft", samplingFrequency)
        return "4/4", fil

    def __three_forth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(int(3 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor(60 / songTempo * samplingFrequency)

        value = 1 / 1
        fil[int(2 * nstep)] = 1 * value

        draw_plot(drawCombFilterPlots, fil, "3/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 3/4 filter dft", samplingFrequency)
        return "3/4", fil

    def __five_forth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(int(5 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor(60 / songTempo * samplingFrequency)

        value = 1 / 3
        fil[int(1 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value
        fil[int(4 * nstep)] = 1 * value

        draw_plot(drawCombFilterPlots, fil, "5/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 5/4 filter dft", samplingFrequency)
        return "5/4", fil
    
    def __six_eigth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(int(3 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor((60 / songTempo * samplingFrequency)/2)

        value = 1 / 2
        fil[int(0 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value

        draw_plot(drawCombFilterPlots, fil, "6/8", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        draw_comb_filter_fft_plot(drawFftPlots, dft, f"Metre 6/8 filter dft", samplingFrequency)
        return "6/8", fil


# %%
signal, samplingFrequency = read_song(song.filepath)

if(resampleSignal):
    signal = scipy.signal.resample(signal, int(len(signal)/resampleRatio))
    samplingFrequency /= resampleRatio
    
sample_length = combFilterPulses * samplingFrequency
seconds = sample_length * 4
draw_plot(drawPlots, signal, f"Song: {song.name}", "Sample/Time", "Amplitude")
song_length = signal.size

start = int(np.floor(song_length / 2 - seconds / 2))
stop = int(np.floor(song_length / 2 + seconds / 2))
if start < 0:
    start = 0
if stop > song_length:
    stop = song_length

sample = signal[start:stop]
draw_plot(drawPlots, sample, f"Sample of: {song.name}", "Sample/Time", "Amplitude")


# %%
centred = center_sample_to_beat(sample, sample_length)
draw_plot(drawPlots, centred, f"Centred to beat: {song.name}", "Sample/Time", "Amplitude")


# %%
print('Filtering song {song.name}...')
filterBanks = prepare_filterbanks(centred, bandLimits, samplingFrequency)
for i in range(0, len(bandLimits)):
    draw_fft_plot(drawPlots, filterBanks[i], f"Filterbank[{i}]{song.name}", samplingFrequency)


# %%
print(f'Windowing song {song.name}...')
hanningWindow = hann(filterBanks, 0.2, bandLimits, samplingFrequency)
draw_plot(drawPlots, hanningWindow[1], f"Hanning Window: {song.name}", "Sample/Time", "Amplitude")


# %%
print(f'Differentiating song {song.name}...')
diffrected = diffrect(hanningWindow, len(bandLimits))
draw_plot(drawPlots, diffrected[1], f"Diffrected: {song.name}", "Sample/Time", "Amplitude")


# %%
print(f'CombFiltering song {song.name}...')
plotDictionary = prepare_plot_dictionary(minBpm, maxBpm)
if useConvolveMethod: 
    tempoDetector = ConvolveTempoDetector()
else:
    tempoDetector = CombFilterTempoDetector()
    
first = tempoDetector.detect_tempo(diffrected,
                      5,
                      minBpm,
                      maxBpm,
                      bandLimits,
                      samplingFrequency,
                      combFilterPulses,
                      plotDictionary)
first


# %%
song_bpm = tempoDetector.detect_tempo(diffrected, 1, first - 5, first + 5, bandLimits, samplingFrequency, combFilterPulses, plotDictionary)
draw_plot(drawSongBpmEnergyPlot, list(plotDictionary.keys()), f"Tempo: {song.name}", "BPM", "Energy", list(plotDictionary.values()))
song_bpm


# %%
metreDetector = DetectMetre()
# metreDetector = DetectMetreNormalized()
# metreDetector = DetectMetreConvolve()
# metreDetector = DetectMetreConvolveNormalized()

metre = metreDetector.detect_metre(diffrected, song_bpm, bandLimits, samplingFrequency, combFilterPulses)
metre


# %%
time = time.time() - startTime
time
