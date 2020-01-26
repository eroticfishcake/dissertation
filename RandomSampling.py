import random 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
import csv
import os

file1 = 'TSLAconverted.csv'

def fileread(file):
    data = pd.read_csv(file)
    return data

def convlists(data):
    df = pd.DataFrame(data)
    lists = df.values
    days = []
    prices = []
    for lis in lists:
        rand = random.random()
        if rand <= 0.7:
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
def scatterfunc(steps, CC, lag, days1, days2, prices1, prices2, average1, average2, std1, std2, N):
    while steps < 360:                                                                             #loop runs till lag is smaller then number of days
        for day in days1:                                                                          #for each day in the list
            Tplus = day + steps                                                                    #day plus positive time lag
            Tminus = day - steps                                                                   #day plus negative time lag
            if Tplus < days1[len(days1) - 1]: 
                if (Tplus in days2) == True:

                    if (day in days1) == True:                                                   #if day plus time lag is less than length of days
                        DCF = ((prices1[days1.index(day)] - average1) * (prices2[days2.index(Tplus)] - average2)) / (std1 * std2)    #calculates DCF
                        CC.append(DCF)                                                                     #puts DCF values into a list with all DCF values at all time lags
                        lag.append(steps)                                                                  #puts time lag values into a list
            if Tminus >= 0: 
                if (Tminus in days2) == True:
                    
                    if (day in days1) == True:  
                                                                                            #if day minus time lag is more than 0 then..
                        DCF = ((prices1[days1.index(day)] - average1) * (prices2[days2.index(Tminus)] - average2)) / (std1 * std2)   #calculates DCF
                        CC.append(DCF)                                                                     #puts DCF values into a list with all DCF values at all time lags
                        lag.append(-steps)                                                                 #puts time lag values into a list
        steps += 1                                                                                 #time lag increases by one
    return lag, CC

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

source = r"C:\Users\modestas\Desktop\dissertation"                              #this is the path to where I keep all my code and csv files
for files in os.walk(source, topdown = True):                                   #goes through every file in the source
    for file2 in files[2]:                                                      #takes only the name of every file
        if file2.find("converted") != -1:                                       #if it finds file that has "converted" in its' name
            if file2.find("TSLA") == -1:
                maxvalues = []
                maxtimelags = []
                variable = 0 
                while variable < 100:   
                                 #if file is not TESLA file
                    path = os.path.join(source, file2[:file2.find("converted")])    #goes into a folder named as the file read
                    steps = 1                                                       #default values needed for functions (time lag at the beginning)
                    CC = []
                    lag = []
                    means = []
                    errors = []
                    lags = []
                    lagcount = -(720/2 - 1)
                    N = 11                                                        #bin size of time lags


                    data1 = fileread(file1)
                    data2 = fileread(file2)

                    days1, prices1 = convlists(data1)
                    days2, prices2 = convlists(data2)

                    std1, std2 = stdev(prices1, prices2)

                    average1, average2 = meanfunc(prices1, prices2)

                    lag, CC = scatterfunc(steps, CC, lag, days1, days2, prices1, prices2, average1, average2, std1, std2, N)

                    lags, means, errors = DCFwerr(means, errors, lags, lagcount, lag, CC, N)

                    plt.errorbar(lags, means, yerr = errors, ecolor = 'black', fmt = '.k')

                    plt.title("Randomly sampled DCF of " + file1[:file1.find("con")] + " and " + file2[:file2.find("con")] + " of bin size " + str(N))

                    plt.ylabel('DCF values')
                    plt.xlabel('time lag (days)')
                    # plt.xlim(89, 129)
                    # plt.ylim(0.7, 1)
                    plt.savefig(os.path.join(path, "Randomly sampled DCF of " + file1[:file1.find("con")] + " and " + file2[:file2.find("con")] + str(N) + ".png"))
                    plt.close()

                    maxvalues.append(max(means))
                    maxtimelags.append(lags[(means.index(max(means)))])
                    print(file2, " loop " ,variable)
                    variable += 1 
                print (maxtimelags)
                height = []
                x = []
                for values in maxtimelags:
                    if (values in x) == False:
                        count = maxtimelags.count(values)
                        height.append(count)
                        x.append(values)


                name = (file2[:file2.find("converted.csv")] + "_PDF.csv")            #name of a new file
                if os.path.isfile(name) == False:                              #if file doesn't already exist in the directory
                    with open(name, 'w', newline = '') as f:                   #creates file
                        for lis in range(len(height)):                      
                            wr = csv.writer(f)                      
                            row = []
                            if (lis == 0):                                     #if it's the first row
                                row.append("time lag")                             #adds name of column
                                row.append("Height")                           #adds name of column
                                wr.writerow(row)                               #saves in the file
                                row = []                                        
                            row.append(x[lis])                         #adds days in the column
                            row.append(height[lis])                       #adds prices in the column 
                            wr.writerow(row)                                   #saves in the file

                plt.bar(x, height)
                plt.title("Probability Density Function of " + file1[:file1.find("con")] + " and " + file2[:file2.find("con")])
                plt.ylabel('maximum peak value count')
                plt.xlabel("time lag (days)")
                plt.savefig(os.path.join(path, "PDF of " + file1[:file1.find("con")] + " and " + file2[:file2.find("con")] + ".png"))
                plt.close()
                    # plt.scatter(lag, CC, s = 0.5)
                    # plt.title(" Random sampling of " + file1[:file1.find("con")] + " and " + file2[:file2.find("con")] + " of bin size " + str(N))
                    # plt.ylabel('Cross correlation values')
                    # plt.xlabel('time lag (days)')
                    # plt.savefig(os.path.join(path, "Random sampling of " + file1[:file1.find("con")] + " and " + file2[:file2.find("con")] + str(N) + ".png"))
                    # plt.close()
                    # #print (file1, " and ", file2)
                    # #print ("peak value ", max(means), " at ", lags[(means.index(max(means)))])
                    # plt.errorbar(lags, means, yerr = errors, ecolor = 'black', fmt = '.k')
                    # plt.title(" Random sampling of " + file1[:file1.find("con")] + " and " + file2[:file2.find("con")] + " of bin size " + str(N))
                    # plt.ylim(-2,1)
                    # plt.ylabel('cross correlation')
                    # plt.xlabel('time lag (days)')
                    # plt.savefig(os.path.join(path, " Final Random sampling of " + file1[:file1.find("con")] + " and " + file2[:file2.find("con")] + str(N) + ".png"))
                    # plt.close()