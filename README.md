# linkedinBot
A bot that uses selenium to log into your linkedin account, and make connection requests using the suggested page.
Requests everyone on the page, and then repeats that for a specified amount of rounds.
#### One request page is one "round".
All of this is done headlessly, so you can use your computer as you please.
Uses the credentials specified by "creds.txt", and logs all activity into "log.txt". These files must be in the
same folder as "connect.py". 

I have mine running as a cron job, at 5 rounds a day (approx. 65 requests a day).
However, I'd suggest trying it out in your command line first. All output to the logfile logs to terminal as well.

## This program requires the following installs:
  - python 2.7 (prob already have this)
  - geckodriver: https://www.npmjs.com/package/geckodriver
  - selenium: "pip install selenium" (if you don't have pip, get pip)
  
## Account safety:
Can't say how this will effect your account's status with Linkedin. I just hacked this together today, and used it
rather recklessly as I was testing it. I would say that if you run it modestly (5 rounds a day), you should be fine. 
I'll update this readme if my account is banned. Enjoy.
