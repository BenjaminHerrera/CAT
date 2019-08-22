# coding=utf-8

"""
Author: 	  Benjamin Herrera
Date Created: 24 April 2018
Date Changed: 13 Augst 2019
"""

# Imports
import os
import sys
import json
import time
import colorama
import subprocess
from time import gmtime 
from time import strftime
from src.api import hitbtc
from src.indicators import bb
from src.indicators import sma
from src.indicators import ema
from src.indicators import rsi
from src.indicators import macd

# Initializes colorama
colorama.init()

# Runs CAT.py
if __name__ == "__main__":

	# Variables
	epoch_num = 0
	error = False
	opportunity = []


	# Checks if HitBTC is reachable
	# Displays whether or not if HitBTC is reachable
	# If not, the program will prompt the user to check internet connection and exits the program
	with open(os.devnull, "wb") as limbo:
		temp = []
		for i in range(1, 101):
			timestamp = "[" + strftime("%d %b %Y %H:%M:%S", gmtime()) + "]"
			result = subprocess.Popen(["ping", "-n", "1", "-w", "200", "1.1.1.1"], stdout=limbo, stderr=limbo).wait()
			print("\r" + timestamp + " Connecting | " + str(i) + "/100 pings tried", end='')
			temp.append(result)
		if not temp[-1]:
			print("\n" + timestamp + "\033[32m Connection established with HitBTC \033[0m")	
		else:
			print("\n" + timestamp + "\033[31m Can not reach HitBTC \033[0m")
			print(timestamp + "\033[31m Check internet connection \033[0m")
			print(timestamp + " Exiting")
			error = True


	# Checks if an error occured
	# If so, exit the script
	if error:
		time.sleep(5)
		exit()


	# Checks if there is any problems with the config file
	# Displays whether or not the config file is corrupted
	# If it is, the program will prompt the user to check the config file
	timestamp = "[" + strftime("%d %b %Y %H:%M:%S", gmtime()) + "]"
	print(timestamp + " Reading configuration file (config.json)")
	try:
		with open('config.json') as file:
			data = json.load(file)
		print(timestamp + " Writing settings to memory")
	except:
		print(timestamp + "\033[31m File is corrupted \033[0m")
		print(timestamp + "\033[31m Check configuration file for errors \033[0m")
		print(timestamp + " Exiting")
		error = True


	# Checks if an error occured
	# If so, exit the script
	if error:
		time.sleep(5)
		exit()


	# Checks if the API Keys are valid
	# Displays whether or not the keys are valid
	# If they are not, the porgram will prompt the user to check the API Keys
	timestamp = "[" + strftime("%d %b %Y %H:%M:%S", gmtime()) + "]"
	print(timestamp + " Checking API keys")
	api = hitbtc.HitBTC(data["keys"]["public"], data["keys"]["private"])
	try:
		if api.get_trading_balance()["error"]["message"] == "Authorization failed":
			print(timestamp + "\033[31m Incorrect API keys \033[0m")
			print(timestamp + "\033[31m Check your API keys \033[0m")
			print(timestamp + " Exiting")
			error = True
	except:
		print(timestamp + " Using public key: " + data["keys"]["public"])
		print(timestamp + " Using private key: " + data["keys"]["private"])


	# Checks if an error occured
	# If so, exit the script
	if error:
		time.sleep(5)
		exit()


	# Make connection to HitBTC's API
	# Creates instances of the indicators
	# EMA, SMA, BB, RSI, MACD
	# Prints message
	api = hitbtc.HitBTC(data["keys"]["public"], data["keys"]["private"])
	timestamp = "[" + strftime("%d %b %Y %H:%M:%S", gmtime()) + "]"
	bb_indicator = bb.BollingerBand(data["indicators"]["bb"]["period"], data["indicators"]["bb"]["multiplier"], None)
	sma_indicator = sma.SimpleMovingAverage(data["indicators"]["sma"]["period"], None)
	ema_indicator = ema.ExponentialMovingAverage(data["indicators"]["ema"]["period"], None)
	rsi_indicator = rsi.RelativeStrengthIndex(data["indicators"]["rsi"]["period"], None)
	macd_indicator = macd.MovingAverageConvergenceDivergence(data["indicators"]["macd"]["fastLength"], data["indicators"]["macd"]["slowLength"], data["indicators"]["macd"]["signalLength"], None)
	print(timestamp + " Apllying indicator settings")

	# Waits 7 seconds
	time.sleep(7)


	# Begins the main part of the script
	# Goes through while loop and goes through markets listed in the config file
	# Calculates values and makes decisions on portfolio
	while True:

		# Variables
		print_line = ""


		# Clears the console
		os.system("cls")
 

		# Increments epoch integer
		# Prints the current epoch
		# Updates timestamp
		epoch_num += 1
		timestamp = "[" + strftime("%d %b %Y %H:%M:%S", gmtime()) + "]"
		print(timestamp + " " + "=" * 12 + "\033[33m EPOCH: " + str(epoch_num) + " \033[0m" + "=" * 12)

		# Applies changes from config file to data
		with open('config.json') as file:
			data = json.load(file)


		# Loops through listed markets in the config file
		for i in data["marketsToTrade"]:

			# Variables
			check_list = []		
			current_close = api.get_candles(i, data["timePeriod"])
			

			# Applies the JSON information to indicator instances
			bb_indicator.set_data_set(current_close)
			sma_indicator.set_data_set(current_close)
			ema_indicator.set_data_set(current_close)
			rsi_indicator.set_data_set(current_close)
			macd_indicator.set_data_set(current_close)


			# Checks if current close is less than or equal to the Bollinger Band's lower band
			# If true, appends a 1 to check_list
			# If not, appends a 0 to check_list
			if data["indicators"]["bb"]["isEnabled"]["buy"] == 1 and float(current_close[:epoch_num+100][-1]) <= bb_indicator.get_lower_band()[-1]:
				check_list.append(1)
			else:
				check_list.append(0)


			# Checks if the market's rsi is lower than 25
			# If true, appends a 1 to check_list
			# If not, appends a 0 to check_list
			if data["indicators"]["rsi"]["isEnabled"]["buy"] == 1 and rsi_indicator.get_relative_strength_index()[-1] <= data["indicators"]["rsi"]["settings"]["lowerTrigger"]:
				check_list.append(1)
			else:
				check_list.append(0)


			# Checks if the market is in an uptrend via MACD
			# If true, appends a 1 to check_list
			# If not, appends a 0 to check_list
			if data["indicators"]["macd"]["isEnabled"]["buy"] == 1 and macd_indicator.get_macd()[-1] < macd_indicator.get_sma_of_signal()[-1]:
				check_list.append(1)
			else:
				check_list.append(0)


			# Checks if the current market iteration is good to buy
			# Updates timestamp
			# Applies restrictor setting
			# Concatenate line variable with current status
			# Appends current market iteration to opportunity list if a buy occurs
			timestamp = "[" + strftime("%d %b %Y %H:%M:%S", gmtime()) + "]"
			if check_list.count(1) >= data["restrictor"]["buy"]:
				print_line = timestamp + " " + i + " \033[32m BUY \033[0m"
				if i not in opportunity:
					opportunity.append(i)
			else:
				print_line = timestamp + " " + i + " \033[34m WAIT \033[0m"

			
			# Checks if the current market iteration is in opportunity list
			# If not, concatenate N\A
			if i in opportunity:

				# Resets the value of the verfication list
				check_list = []


				# Checks if current close is greater than or equal to the Bollinger Band's upper band
				# If true, appends a 1 to check_list
				# If not, appends a 0 to check_list
				if data["indicators"]["bb"]["isEnabled"]["sell"] == 1 and float(current_close[:epoch_num+100][-1]) >= bb_indicator.get_lower_band()[-1]:
					check_list.append(1)
				else:
					check_list.append(0)


				# Checks if the market's rsi is higher than or equal to 70
				# If true, appends a 1 to check_list
				# If not, appends a 0 to check_list
				if data["indicators"]["rsi"]["isEnabled"]["sell"] == 1 and rsi_indicator.get_relative_strength_index()[-1] >= data["indicators"]["rsi"]["settings"]["upperTrigger"]:
					check_list.append(1)
				else:
					check_list.append(0)


				# Checks if the market is in an downtrend via MACD
				# If true, appends a 1 to check_list
				# If not, appends a 0 to check_list
				if data["indicators"]["macd"]["isEnabled"]["sell"] == 1 and macd_indicator.get_macd()[-1] > macd_indicator.get_sma_of_signal()[-1]:
					check_list.append(1)
				else:
					check_list.append(0)


				# Checks if the current market iteration is good to sell
				# Applies restrictor setting
				# Concatenate line variable with current status
				# Remove current market iteration to opportunity list if a sell occurs
				if check_list.count(1) >= data["restrictor"]["sell"]:
					print_line += "\031[32m SELL \031[0m"
					if i in opportunity:
						opportunity.remove(i)
				else:
					print_line += "\033[34m WAIT \033[0m"

			else:
				print_line += " N\\A"


			# Prints status of market 
			print(print_line)

		# Waits for 5 seconds
		time.sleep(5)