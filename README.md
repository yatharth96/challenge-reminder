# challenge-reminder
Get text reminders for upcoming coding challenges.

### Version
 - Python 2.7.x

### Requirements
 - Twilio [account](https://www.twilio.com/) with your mobile number activated.
 - twilio (```$pip install twilio ```)
 - selenium (```$ pip install selenium```)
 - Beautiful Soup (```$ pip install bs4```)
 - [PhantomJS](http://phantomjs.org/download.html)

### Usage
1. Clone/Download main.py
2. For **Windows**:Using *Windows Task Scheduler* add the script to run everytime at reboot/user login.
3. For **Linux**:Using *cron* set the script to run automatically at reboot/user logi.n
4. Run the script and add the time at which you want to get notified.
5. In future if you wish to change the timings,go to directory with main.py and delete **timings.txt** and repeat *step 4*.
