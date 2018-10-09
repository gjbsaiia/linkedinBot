#!/usr/bin/python

# Griffin Saiia, gjs64@case.edu
# github: https://github.com/gjbsaiia

import os
import sys
import time
from datetime import datetime, timedelta
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class analytics:
	def __init__(self):
		self.i = 0
		self.fcount = 0
		self.connections = 0
		self.start = 0
		self.stop = 0
		self.totalTime = ""
	def iPlusOne(self):
		self.i += 1
	def newFail(self):
		self.fcount += 1
	def newConnect(self):
		self.connections += 1
	def startTime(self):
		sta = datetime.now()
		self.start = timedelta(hours=sta.hour,minutes=sta.minute,seconds=sta.second)
	def stopTime(self):
		sto = datetime.now()
		self.stop = timedelta(hours=sto.hour,minutes=sto.minute,seconds=sto.second)
		self.totalTime = str(self.stop-self.start)

def main():
	with open("creds.txt", "r") as file:
		lines = file.readlines()
	file.close()
	user = lines[0].split("username = ")[1]
	password = lines[1].split("password = ")[1]
	limit = int(lines[2].split("rounds = ")[1])
	round = analytics()
	round.startTime()
	with open("log.txt", "a") as file:
		file.write("Session started at "+str(round.start)+"... \n")
		file.write("\n")
	file.close()
	print("Linkedin Linker running...\n")
	process(user, password, round, limit)
	round.stopTime()
	print("")
	print("...Finished at "+str(round.stop)+".")
	print("Bot failed "+str(round.fcount)+" times.")
	print("Made "+str(round.connections)+" connections in "+round.totalTime+".")
	with open("log.txt", "a") as file:
		file.write("\n")
		file.write("...Finished at "+str(round.stop)+".\n")
		file.write("Bot failed "+str(round.fcount)+" times.\n")
		file.write("Made "+str(round.connections)+" connections in "+round.totalTime+".\n")
	file.close()

def process(user, password, round, limit):
	options = Options()
	options.set_headless(headless=True)
	driver = webdriver.Firefox(firefox_options=options)
	driver.get("https://www.linkedin.com")
	element = driver.find_element_by_id("dismiss-alert")
	element.click()
	element = driver.find_element_by_class_name("login-email")
	element.send_keys(user)
	element = driver.find_element_by_class_name("login-password")
	element.send_keys(password)
	element = driver.find_element_by_id("login-submit")
	element.click()
	try:
		element = driver.find_element_by_id("mynetwork-tab-icon")
		element.click()
		print("Logged in...\n")
		with open("log.txt", "a") as file:
			file.write("Logged in...\n")
		file.close()
	except selenium.common.exceptions.NoSuchElementException:
		print("Login failed.\n")
		with open("log.txt", "a") as file:
			file.write("Login failed.\n")
		file.close()
		raise KeyboardInterrupt
	try:
		name = ""
		lastname = ""
		while(round.i < limit):
			print("  Round "+str(round.i)+":")
			with open("log.txt", "a") as file:
				file.write("  Round "+str(round.i)+": \n")
			file.close()
			while True:
				try:
					if(driver.current_url == "https://www.linkedin.com/mynetwork/"):
						element = driver.find_element_by_class_name("pymk-card__name")
						name = element.text
						if(name != lastname):
							print("    Requested to connect with "+name+".")
							with open("log.txt", "a") as file:
								file.write("    Requested to connect with "+name+".\n")
							file.close()
							round.newConnect()
						element = driver.find_element_by_css_selector("button.button-secondary-small")
						element.click()
						lastname = name
						time.sleep(0.35)
					else:
						round.newFail()
						driver.get("https://www.linkedin.com/mynetwork/")
				except selenium.common.exceptions.NoSuchElementException:
					break
			round.iPlusOne()
			driver.refresh()
		driver.close()
	except selenium.common.exceptions.WebDriverException:
		driver.close()
		round.newFail()
		print("")
		print("...Kicked out, :[")
		print("Picking up where we left off...\n")
		with open("log.txt", "a") as file:
			file.write("\n")
			file.write("...Kicked out, :[\n")
			file.write("Picking up where we left off...\n")
			file.write("\n")
		file.close()
		process(user, password, round, limit)


#Execute the wrapper
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print 'Interrupted'
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
