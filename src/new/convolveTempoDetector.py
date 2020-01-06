import numpy as np
import plots
import settings
import scipy.signal

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
            plots.draw_fft_plot(settings.drawFftPlots, dft[band], f"Band[{band}] DFT", samplingFrequency)
    
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
    
            plots.draw_plot(settings.drawCombFilterPlots, fil, f"Timecomb bpm: {bpm}", "Sample/Time", "Amplitude")
    
            # Get the filter in the frequency domain
            dftfil = np.fft.fft(fil)
            # dftfil = scipy.signal.resample(dftfil, len(dft[0]))
    
            plots.draw_comb_filter_fft_plot(settings.drawCombFilterPlots, dftfil, f"Filter DFT {bpm}", samplingFrequency)
            for band in range(0, nbands-1):
                filt = scipy.convolve(signal[band], fil)
                f_filt = abs(np.fft.fft(filt))
                plots.draw_fft_plot(settings.drawFftPlots, f_filt, f"Convolve DFT {bpm}", samplingFrequency)
    
                x = abs(f_filt)**2
                e = e + sum(x)
    
    
            plotDictionary[bpm] = e
            # If greater than all previous energies, set current bpm to the bpm of the signal
            if e > maxe:
                sbpm = bpm
                maxe = e
    
        return sbpm
