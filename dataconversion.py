import pandas as pd
import numpy as np
import statistics
from datetime import datetime
import numpy as np
import os
import csv

a = []
daystesla = []
pricestesla = []
times = []
timesreal = []
var = 0
count = 0

file1 = 'ASGLY.csv'

def fileread(file):
    data = pd.read_csv(file, usecols = ['Date', 'Close'])
    return data

def pricearray(a, data):
    for price in data['Close']:
        a.append(price)  
    return a

def dateconverter(date, times, timesreal, count):
    epochtime = datetime.fromisoformat(date).timestamp() #converting from calendar date to seconds from the epoch start
    times.append(epochtime) 
    days = (times[count] - times[0])/60/60/24 #converting to days and taking first date as a reference point
    timesreal.append(int(days))
    return timesreal
    
def lininterpolation(timesreal, pricelist, var):
    x1 = timesreal[var]
    x0 = timesreal[var - 1]
    y1 = pricelist[var]
    y0 = pricelist[var - 1]
    x = int(x0 + 1)
    y = (y0 * (x1 - x) + y1 * (x - x0)) / (x1 - x0)
    return x, y

def insertprices(data, var, count, pricelist, timesreal, times):      
    for date in data['Date']: #reading all the data of the column labeled 'Date'   
        realtime = dateconverter(date, times, timesreal, count)
        if var >= 1:
            difference = int(realtime[var] - realtime[var - 1])
            while difference != 1:
                x, y = lininterpolation(realtime, pricelist, var)                
                realtime.insert(var, x)
                pricelist.insert(var, y)
                var += 1
                difference = int(realtime[var] - realtime[var - 1])
        var += 1
        count += 1
    return realtime, pricelist

def stdev(pricelist):
    standartdeviation = np.std(pricelist)
    return standartdeviation

def filewrite(file):
    data = pd.write_csv(file)
    return data

data = fileread(file1)
pricelist = pricearray(a, data)
daystesla, pricestesla = insertprices(data, var, count, pricelist, timesreal, times)

print (len(pricestesla))
print (len(daystesla))

name = input('write a file name: ')
if os.path.isfile(name) == False:
    with open(name, 'w', newline = '') as f:
        for lis in range(len(daystesla)):
            wr = csv.writer(f)
            row = []
            if (lis == 0):
                row.append("Days")
                row.append("Prices")
                wr.writerow(row)
                row = []
            row.append(daystesla[lis])
            row.append(pricestesla[lis])
            wr.writerow(row)