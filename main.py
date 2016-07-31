from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import time
import re
import sys
import os

URL="http://codingcalendar.com/upcoming"
# Enter your twilio credentials here
accountSID="################"
authToken ="################"

# Enter the path to phantomjs here
PATH="####################################"

# Enter our mobile number and twilio number here
MOBILE_NUMBER="############"
TWILIO_NUMBER="############"

db=[]
out=[]

def create():
    global client
    client=TwilioRestClient(accountSID,authToken)

def get_time(time):
    time_obj=datetime.datetime.strptime(time,"%a %b %d %Y %H:%M")
    return time_obj

def calculate():
    current=datetime.datetime.now()
    upper_bound=current+datetime.timedelta(days=1)
    for item in db:
        if item["timeObj"]<upper_bound:
            out.append(item)

def file_handle():
    try:
        fh=open("timings.txt",'r')
        content1=fh.read()
        if content1!="":
            content=datetime.datetime.strptime(content1,"%Y-%m-%d %H:%M:%S")
    except IOError:
        fh=open("timings.txt",'w')
        content1=""
    times=""
    if len(content1)==0:
        times=raw_input("Enter the time at which you want the script to run daily? [hh:mm]")
        temp=str(datetime.date.today())+" "+times
        times_obj=datetime.datetime.strptime(temp,"%Y-%m-%d %H:%M")
        content=times_obj
    fh.close()

    fh=open("timings.txt",'w')
    nextday=content+datetime.timedelta(days=1)
    fh.write(str(nextday))
    fh.close()
    return content

def file_update():
    fh=open("timings.txt",'w')
    if times:
        fh.write(str(times_obj))
    else:
        nextday=content+datetime.timedelta(days=1)
        fh.write(str(nextday))
    fh.close()
    return content


def get_data():
    driver=webdriver.PhantomJS(executable_path=PATH)
    driver.get(URL)
    time.sleep(3)
    data=driver.page_source
    soup=BeautifulSoup(data,'html')
    infos=soup.find_all(class_="post-preview")

    for info in infos:
        title=str(info.find(class_="post-title").text)
        duration=str(info.find(class_="post-subtitle").text)
        otherinfo=str(info.find(class_="post-meta").text)
        timeobj=get_time(otherinfo.partition("Starts: ")[2])
        db.append({"Title":title,"Duration":duration,"others":otherinfo,"timeObj":timeobj})
        
def create_body():
    cnt=0
    f=open("content.txt",'w')
    f.write("List of upcoming contests in upcoming 24 hours\n")
    for o in out:
        cnt+=1
        f.write(str(cnt)+". "+o["Title"]+"\n")
        f.write("   Duration: "+o["Duration"]+"\n")
        f.write("   "+o['others']+"\n")
    f.close()

def read_body():
    f=open("content.txt",'r')
    body=f.read()
    return body
        
        
        
def send_message():
    material=read_body()
    
    try:
        print "Sending.."
        client.messages.create(body=material,to=MOBILE_NUMBER,from_=TWILIO_NUMBER)
        print "Done!"
    except TwilioRestException as e:
        print "Error",e

def main():
    startTime=file_handle()
    print "Path to timings.txt : ", os.path.join(os.getcwd(),'timings.txt')
    while datetime.datetime.now()<startTime:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print "Program stopped by user!"
            print "Exiting!"
            sys.exit()
    get_data()
    calculate()
    create()
    create_body()
    send_message()

if __name__=='__main__':
    main()
    
