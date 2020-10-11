import speedtest as st
from csv import writer
from datetime import datetime
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt

#const
filename = "internet_speeds_dataset.csv"

#can remove this parameter for infinite speed test and data collection
period = 3*60*60
delay = 4*60
n = 45/delay



# Get speedtest values
def get_new_speeds():
    speed_test = st.Speedtest()
    speed_test.get_best_server()
    # Get ping (miliseconds)
    ping = speed_test.results.ping
    # Perform download and upload speed tests (bits per second)
    download = speed_test.download()
    upload = speed_test.upload()
    # Convert download and upload speeds to megabits per second
    download = round(download / (10**6), 2)
    upload = round(upload / (10**6), 2)
    return (ping, download, upload)

#create .csv file to store dataset
def createfile():
    header = ("Date", "Time", "Ping", "Download", "Upload")
    with open(filename, "w", newline ="") as csvfile:
        speeddata = csv.writer(csvfile)
        speeddata.writerow(header)

#update speedtest results to .csv file
def update_csv(internet_speeds,filename):
    # Get today's date in the form Day/Month/Year
    date_today = datetime.today().strftime("%d/%m/%Y")
    #Get time now in form of Hour:Minute:second
    now = datetime.now()
    time_now = now.strftime("%H:%M:%S")
    # Open csv file
    with open(filename, 'a+' , newline= "") as file:
        csv_writer = writer(file)
        # Append data
        data = [date_today, time_now, internet_speeds[0],internet_speeds[1], internet_speeds[2]]
        csv_writer.writerow(data)

#To iterate subsets of dataset
def iterate (piece,n,mean,tolerance):
    count = 0
    for index, row in piece.iterrows():
        if (row.Download > (mean.Download - tolerance)):
            count = count + 1
    if (count == n):
        return(piece.mean())
    else :
        return mean

#To monitor speed
def monitor(plan):
    check = 0
    i=0
    prev_i =0
    #Infinite loop to obtain dataset
    while True:
        i = i+1
        new_speeds = get_new_speeds()
        update_csv(new_speeds,filename)
        tolerance = (plan*5)/100
        #Alert
        if (new_speeds[1] < (plan-tolerance)):
            if (i == prev_i+1):
                check = check+1
                prev_i = i
                if(check == (10*60)/delay):
                    return True         
        time.sleep(delay)

#To cretae graph for display
def plot_data():
    col_list = ["Time","Ping","Download","Upload"]
    data = pd.read_csv(filename, usecols=col_list)

    #Plot data
    x = data.Time
    y = data.Download
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y,'o-')
    fig.autofmt_xdate()
    plt.savefig('image.png')

#Find optimum time
def optimum(plan):
    col_list = ["Time","Ping","Download","Upload"]
    data = pd.read_csv(filename, usecols=col_list)
    mean = data.mean()
    tolerance = (plan*5)/100

    count = 0
    length = len(data.index)
    top = data[0:3]
    temp = data[0:n]
    maxmean = temp.mean()

    #Checking for highest flat region
    for index, row in data.iterrows():
        if (index > length-n):
            break
        tempmean = iterate(data[index:index+n],n,mean,tolerance)

        if (tempmean.Download >= maxmean.Download):
            maxmean.Download = tempmean.Download
            top = data[index:index+n]
    time1 = top.iloc[0]
    time2 = top.iloc[-1]
    return(time1.Time,time2.Time)