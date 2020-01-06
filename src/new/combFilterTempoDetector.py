import numpy as np
import plots
import settings


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
            plots.draw_fft_plot(settings.drawFftPlots, dft[band], f"Band[{band}] DFT", samplingFrequency)
    
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
    
            plots.draw_plot(settings.drawCombFilterPlots, fil, f"Timecomb bpm: {bpm}", "Sample/Time", "Amplitude")
            # Get the filter in the frequency domain
            dftfil = np.fft.fft(fil)
            plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dftfil, f"Filter's signal DFT {bpm}", samplingFrequency)
    
            for band in range(0, bands_amount):
                x = (abs(dftfil * dft[band])) ** 2
                this_bpm_energy = this_bpm_energy + sum(x)
    
            plotDictionary[bpm] = this_bpm_energy
            # If greater than all previous energies, set current bpm to the bpm of the signal
            if this_bpm_energy > maxEnergy:
                songBpm = bpm
                maxEnergy = this_bpm_energy
    
        return songBpm
