import speedtest as st
from csv import writer
from datetime import datetime
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt

#TO-DO: Enter any file name with .csv extention
filename = "internet_speeds_dataset.csv"
#TO-DO: To set speed update interval in seconds
delay = 4*60
#TO-DO: To sent duration for surfing. To get best stable speed interval
n = int((20*60)/delay)

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

#update speedtest results to .csv file
def update_csv(internet_speeds,filename):
    date_today = datetime.today().strftime("%d/%m/%Y")
    now = datetime.now()
    time_now = now.strftime("%H:%M:%S")
    with open(filename, 'a+' , newline= "") as file:
        csv_writer = writer(file)
        # Append data
        data = [date_today, time_now, internet_speeds[0],internet_speeds[1], internet_speeds[2]]
        csv_writer.writerow(data)

#create .csv file to store dataset
def createfile():
    header = ("Date", "Time", "Ping", "Download", "Upload")
    with open(filename, "w", newline ="") as csvfile:
        speeddata = csv.writer(csvfile)
        speeddata.writerow(header)

#To iterate subsets of dataset (call form optimum_time function)
def iterate(piece,n,mean,tolerance):
    count = 0
    for index, row in piece.iterrows():
        if (row.Download > (mean.Download - tolerance)):
            count = count + 1
    if (count == n):
        return(piece.mean())
    else :
        return mean

#To monitor speed
def monitor():
    while True:
        new_speeds = get_new_speeds()
        update_csv(new_speeds,filename)       
        time.sleep(delay)

#To cretae graph for display
def plot_data():
    print("plotting")
    col_list = ["Time","Ping","Download","Upload"]
    data = pd.read_csv(filename, usecols=col_list)
    #Plot data
    x = data.Time
    y = data.Download
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y,'o-')
    fig.autofmt_xdate()
    #TO_DO:Enter loaction for storing plot image
    plt.savefig('image.png')

#Find optimum time
def optimum_time():
    col_list = ["Time","Ping","Download","Upload"]
    data = pd.read_csv(filename, usecols=col_list)
    mean = data.mean()
    high_tolerance = ((10*mean.Download)/100)
    count = 0
    length = len(data.index)
    top = data[0:3]
    temp = data[0:n]
    maxmean = temp.mean()
    #Checking for highest flat region
    for index, row in data.iterrows():
        if (index > length-n):
            break
        tempmean = iterate(data[index:index+n],n,mean,high_tolerance)
        if (tempmean.Download >= maxmean.Download):
            maxmean.Download = tempmean.Download
            top = data[index:index+n]
    time1 = top.iloc[0]
    time2 = top.iloc[-1]
    return(time1.Time,time2.Time)

def send_alert(value):
    plan = int(value)
    col_list = ["Time","Ping","Download","Upload"]
    data = pd.read_csv(filename, usecols=col_list)
    mean = data.mean()
    tolerance = (plan*5)/100
    length = len(data.index)
    check_set = data[length-1:length+1]
    check_set_mean = check_set.mean()
    if (check_set_mean.Download < (plan-tolerance)):    
        return ("True")
    else :
        return ("False")