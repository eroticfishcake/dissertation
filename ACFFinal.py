import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import os

#reads a date and close price columns from csv file
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

def stdev(pricelist1, pricelist2):
    standartdeviation1 = np.std(pricelist1)
    standartdeviation2 = np.std(pricelist2)
    return standartdeviation1, standartdeviation2

def meanfunc(prices1, prices2):
    average1 = sum(prices1)/len(prices1)
    average2 = sum(prices2)/len(prices2)
    return average1, average2

#function for getting unbinned DCF
def scatterfunc(steps, CC, lag, days1, prices1, prices2, average1, average2, std1, std2, N):
    while steps < 360:                                                                             #loop runs till lag is smaller then number of days
        for day in days1:                                                                          #for each day in the list
            Tplus = day + steps                                                                    #day plus positive time lag
            Tminus = day - steps                                                                   #day plus negative time lag
            if Tplus < len(days1):                                                                 #if day plus time lag is less than length of days
                DCF = ((prices1[day] - average1) * (prices2[Tplus] - average2)) / (std1 * std2)    #calculates DCF
                CC.append(DCF)                                                                     #puts DCF values into a list with all DCF values at all time lags
                lag.append(steps)                                                                  #puts time lag values into a list
            if Tminus >= 0:                                                                        #if day minus time lag is more than 0 then..
                DCF = ((prices1[day] - average1) * (prices2[Tminus] - average2)) / (std1 * std2)   #calculates DCF
                CC.append(DCF)                                                                     #puts DCF values into a list with all DCF values at all time lags
                lag.append(-steps)                                                                 #puts time lag values into a list
        steps += 1                                                                                 #time lag increases by one
    return lag, CC

#bins up all the DCF values at each time lag and gets one average value
def DCFwerr(means, errors, lags, lagcount, lag, CC, N):
    while lagcount < 360:                                               #loop runs till lag is smaller then number of days
        binsize = N                                                     #binning up of time lags, where N is the variable that defines the size of a bin
        CCs = []
        while binsize >= 1:                                             
            index = 0
            for i in lag:                                               #for every time lag in lags list
                if i == lagcount:                                       #if time lag is equal to lagcount variable
                     CCs.append(CC[index])                              #append all DCF values at that time lag to CCs list
                index += 1                                      
            lagcount += 1                                               #lagcount variable increases
            binsize -= 1                                                #binsize value decreases
        if len(CCs) != 0:                                               #if list is not empty
            avrg = sum(CCs)/len(CCs)                                    #calculates the average of that list
            means.append(avrg)                                          #adds that average to another list of averages
            std = np.std(CCs)
            errors.append(std)  
            lags.append(lagcount - 1)                                   #appends time lag value

    return lags, means, errors
N = 1
source = r"C:\Users\modestas\Desktop\dissertation"                              #this is the path to where I keep all my code and csv files
while N <= 20:
    for files in os.walk(source, topdown = True):                                   #goes through every file in the source
        for file2 in files[2]:                                                      #takes only the name of every file
            if file2.find("converted") != -1:                                       #if it finds file that has "converted" in its' name
                file1 = file2
                path = os.path.join(source, file2[:file2.find("converted")])    #goes into a folder named as the file read
                steps = 1                                                       #default values needed for functions (time lag at the beginning)
                CC = []
                lag = []
                means = []
                errors = []
                lags = []
                lagcount = -(720/2 - 1)


                data1 = fileread(file1)
                data2 = fileread(file2)

                days1, prices1 = convlists(data1)
                days2, prices2 = convlists(data2)

                std1, std2 = stdev(prices1, prices2)
                print (file2[:file2.find("con")] + " standart deviation", std1)
                average1, average2 = meanfunc(prices1, prices2)

                lag, CC = scatterfunc(steps, CC, lag, days1, prices1, prices2, average1, average2, std1, std2, N)
                lags, means, errors = DCFwerr(means, errors, lags, lagcount, lag, CC, N)
                
                plt.scatter(lag, CC, s = 0.5)
                plt.title(" Auto Correlation Function of " + file1[:file1.find("con")] + " of bin size " + str(N))
                plt.ylabel('Auto correlation values')
                plt.xlabel('time lag (days)')
                plt.savefig(os.path.join(path, "Auto Correlation function of " + file1[:file1.find("con")]  + str(N) + ".png"))
                plt.close()
                
                plt.errorbar(lags, means, yerr = errors, ecolor = 'black', fmt = '.k')
                plt.title(" Auto Correlation Function of " + file1[:file1.find("con")] + " of bin size " + str(N))
                #plt.ylim()
                plt.ylabel('Auto correlation values')
                plt.xlabel('time lag (days)')
                plt.savefig(os.path.join(path, " Final Auto correlation function of " + file1[:file1.find("con")] + str(N) + ".png"))
                plt.close()
    N += 2