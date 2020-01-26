import pandas as pd
import numpy as np
from scipy.fftpack import fft
from statistics import mean
import math
import matplotlib.pyplot as plt
import os

plt.ioff()

def fileread(file):
    data = pd.read_csv(file)
    return data

def convlists(data):
    df = pd.DataFrame(data)
    lists = df.values
    days = []
    prices = []
    for lis in lists:
        days.append(int(lis[0]))
        prices.append(lis[1])
    return days, prices

def stdev(pricelist):
    standartdeviation1 = np.std(pricelist)
    return standartdeviation

def best_fit_slope_and_intercept(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
    b = mean(ys) - m*mean(xs)
    
    return m, b

def logconv(frequency, logf, power, fourierprices):
    count = 0
    for f in frequency:
        if f != 0:
            log10f = math.log10(f)
            logf.append(log10f)
            log10power = math.log10(abs(fourierprices[count] ** 2))
            power.append(log10power)
        count += 1
        
    return power, logf

def binpowerspectrum(bins, std, binfrequency, xerr):
    N = 1
    index = 0
    onebin = []
    for i in logf:
        if i < (logf[0] + (binsize * N)):   #if datapoint is inside the bin
            onebin.append(power[index])     #append that datapoint to a list "onebin" 
        if i >= (logf[0] + (binsize * N)):  #if datapoint is outside the bin
            onebin.append(power[index])     #append the last datapoint that is inside the bin
            bins.append((sum(onebin)/len(onebin)))#append a mean value of binned values to another list "bins"
            std.append(np.std(onebin)) #getting standart deviation of the binned values
            onebin = []                #emptying the bin
            binfrequency.append(logf[0] + (binsize * (N - 1) + (((binsize * N) - (binsize * (N - 1))) / 2))) #getting the middle value of each bin
            N += 1    #next bin
        index += 1    #index increases
        
    return bins, binfrequency, std

# def offset(binnumber, xerr):
#     for numbers in range(binnumber):
#         xerr.append(0.255)
#     return xerr

source = r"C:\Users\modestas\Desktop\dissertation"
for files in os.walk(source, topdown = True):
    for file in files[2]:
        if file.find("converted") != -1:
            path = os.path.join(source, file[:file.find("converted")])
            if os.path.exists(path) == False:
                os.mkdir(path)

                logf = []
                power = []
                bins = []
                std = []
                binfrequency = []
                xerr = []

                data = fileread(file)

                days, prices = convlists(data)

                fourierprices = fft(prices)

                plt.scatter(days[2:-1], fourierprices[2:-1], s = 0.5)
                plt.plot(days[2:-1], fourierprices[2:-1], '-o')
                #plt.ylim(-1000,2000)
                plt.title("fAmplitudes against Time of " + file[:file.find("con")])
                plt.ylabel('Amplitudes')
                plt.xlabel('Time (days)')
                plt.savefig(os.path.join(path, "fourier transformed prices vs. time in days of " + file[:file.find("con")] + "1" + ".png"))
                plt.close()

                plt.plot(days[2:-1], fourierprices[2:-1])
                #plt.ylim(-1000,2000)
                plt.title("Amplitudes against Time of " + file[:file.find("con")])
                plt.ylabel('Amplitudes')
                plt.xlabel('Time (days)')
                plt.savefig(os.path.join(path, "fourier transformed prices vs. time in days of " + file[:file.find("con")] + "2" + ".png"))
                plt.close()

                T = 86400
                frequency = np.linspace(0, 1 / T, len(days))

                plt.plot(frequency[2:len(days) // 2], fourierprices[2:len(days) // 2], '-o')
                plt.title("Amplitudes against Frequency of " + file[:file.find("con")])
                #plt.ylim(-1000,2000)
                plt.ylabel('Amplitudes')
                plt.xlabel('Frequency (Hz)')
                plt.savefig(os.path.join(path, "fourier transformed prices vs. frequency in Hz " + file[:file.find("con")] + "1" + ".png"))
                plt.close()

                plt.plot(frequency[2:len(days) // 2], fourierprices[2:len(days) // 2])
                plt.title("Amplitudes against Frequency of " + file[:file.find("con")])
                #plt.ylim(-1000,2000)
                plt.ylabel('Amplitudes')
                plt.xlabel('Frequency (Hz)')
                plt.savefig(os.path.join(path, "fourier transformed prices vs. frequency in Hz " + file[:file.find("con")] + "2" + ".png"))
                plt.close()

                power, logf = logconv(frequency, logf, power, fourierprices)

                plt.plot(logf[:len(days) // 2], power[:len(days) // 2], '-o')
                plt.title("Power Spectrum of " + file[:file.find("con")])
                plt.ylabel('log power')
                plt.xlabel('log frequency (Hz)')
                plt.savefig(os.path.join(path, "power spectrum of " + file[:file.find("con")] + "1" + ".png"))
                plt.close()

                plt.plot(logf[:len(days) // 2], power[:len(days) // 2])
                plt.title("Power Spectrum of " + file[:file.find("con")])
                plt.ylabel('Log Power')
                plt.xlabel('Log Frequency (Hz)')
                plt.savefig(os.path.join(path, "power spectrum of " + file[:file.find("con")] + "2" + ".png"))
                plt.close()

                logf = logf[:len(days) // 2]
                power = power[:len(days) // 2]
                rangef = logf[-1] - logf[0]
                binnumber = 7
                binsize = rangef / binnumber

                bins, binfrequency, std = binpowerspectrum(bins, std, binfrequency, xerr)
                #xerr = offset(binnumber, xerr)
                binsfinal = []
                for bi in bins:
                    binsfinal.append(bi + 0.253)
                xs = np.array(binfrequency, dtype=np.float64)
                ys = np.array(binsfinal, dtype=np.float64)

                m, b = best_fit_slope_and_intercept(xs, ys)

                regression_line = [(m*x)+b for x in xs]

                print(file[:file.find("con")], (8 - len(file[:file.find("con")])) * " ", "y =",round(m,6), "* x",round(b,7), "|", "uncertainty in slope :", ((max(binsfinal)/min(binfrequency))-(min(binsfinal)/max(binfrequency)))/2)

                plt.errorbar(binfrequency, binsfinal, std, ecolor = 'black', fmt = '.k')
                plt.title("Binned up Power Spectrum of " + file[:file.find("con")])
                plt.ylabel("Log Power")
                plt.xlabel("Log Frequency")
                plt.plot(xs, regression_line, color='red')
                plt.savefig(os.path.join(path, "binned power spectrum of " + file[:file.find("con")] + ".png"))
                plt.close()
