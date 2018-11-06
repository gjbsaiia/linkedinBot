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


class session:
	def __init__(self):
		self.driver = None
		self.username = ""
		self.password = ""
		self.lastAdded = ""
		self.limit = ""
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
		self.start = timedelta(hours=sta.hour, minutes=sta.minute, seconds=sta.second)

	def stopTime(self):
		sto = datetime.now()
		self.stop = timedelta(hours=sto.hour, minutes=sto.minute, seconds=sto.second)
		self.totalTime = str(self.stop-self.start)


elemDic = {
	"url": "https://www.linkedin.com",
	"myURL": "https://www.linkedin.com/mynetwork/",
	"alrt": "dismiss-alert",
	"usr": "login-email",
	"pswd": "login-password",
	"sub": "login-submit",
	"myNet": "mynetwork-tab-icon",
	"connect": "button.button-secondary-small",
	"connectName": "pymk-card__name"
}


def main():
	with open("creds.txt", "r") as file:
		lines = file.readlines()
	file.close()
	round = session()
	round.username = lines[0].split("username = ")[1]
	round.password = lines[1].split("password = ")[1]
	round.limit = int(lines[2].split("rounds = ")[1])
	round.startTime()
	with open("log.txt", "a") as file:
		file.write("Session started at "+str(round.start)+"... \n")
		file.write("\n")
	file.close()
	print("Linkedin Linker running...\n")
	link(round)
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


def link(round):
	start(round)
	try:
		name = ""
		while(round.i < round.limit):
			print("  Round "+str(round.i)+":")
			with open("log.txt", "a") as file:
				file.write("  Round "+str(round.i)+": \n")
			file.close()
			connections = loadNew(round)
			made = 0
			while (made != connections):
				try:
					made += loop(round)
				except selenium.common.exceptions.NoSuchElementException:
					break
			round.iPlusOne()
			round.driver.refresh()
		round.driver.close()
	except selenium.common.exceptions.WebDriverException:
		kicked(round)


def start(round):
	options = Options()
	options.set_headless(headless=True)
	round.driver = webdriver.Firefox(firefox_options=options)
	round.driver.get(elemDic["url"])
	try:
		element = round.driver.find_element_by_id(elemDic["alrt"])
		element.click()
	except selenium.common.exceptions.NoSuchElementException:
		k = 0
	element = round.driver.find_element_by_class_name(elemDic["usr"])
	element.send_keys(round.username)
	element = round.driver.find_element_by_class_name(elemDic["pswd"])
	element.send_keys(round.password)
	element = round.driver.find_element_by_id(elemDic["sub"])
	element.click()
	try:
		element = round.driver.find_element_by_id(elemDic["myNet"])
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


def loadNew(round):
	if(round.driver.current_url == elemDic["myURL"]):
		elements = round.driver.find_elements_by_css_selector(elemDic["connect"])
		connections = len(elements)
		while(connections == 0):
			round.driver.refresh()
			if(round.driver.current_url != elemDic["myURL"]):
				round.driver.get(elemDic["myURL"])
			elements = round.driver.find_elements_by_css_selector(elemDic["connect"])
			connections = len(elements)
		return connections
	else:
		round.driver.get(elemDic["myURL"])
		return loadNew(round)


def loop(round):
	made = 0
	if(round.driver.current_url == elemDic["myURL"]):
		element = round.driver.find_element_by_class_name(elemDic["connectName"])
		name = element.text
		if(name != round.lastAdded):
			print("    Requested to connect with "+name+".")
			with open("log.txt", "a") as file:
				try:
					file.write("    Requested to connect with "+name+".\n")
				except UnicodeEncodeError:
					file.write("    Requested to connect with "+name.encode('ascii', 'ignore')+".\n")
			file.close()
			round.newConnect()
			made += 1
		element = round.driver.find_element_by_css_selector(elemDic["connect"])
		element.click()
		round.lastAdded = name
		time.sleep(0.35)
	else:
		round.newFail()
		round.driver.get(elemDic["myURL"])
	return made


def kicked(round):
	round.driver.close()
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
	link(round)


# Execute the wrapper
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print
		print 'Interrupted \_[o_0]_/'
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
