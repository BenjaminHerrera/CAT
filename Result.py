#coding=utf-8

"""
Author: Benjamin Herrera
Date Created: 8 August 2019
Date Changed: 21 August 2019
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

# Runs Result.py
if __name__ == "__main__":

	# Variables
	portfolio = 10.0
	start_price = 0	
	end_price = 0
	epoch_num = 0
	trades = 0
	opportunity = False
	entered = False	
	error = False
	close_data = []


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

	# Grabs information from specified data set
	# Places information to a variable
	with open('data/' + str(sys.argv[1])) as file:
		data_set = json.load(file)


	# Creates a list of close values
	for i in data_set:
		close_data.append(float(i['close']))

 	
	# Make connection to HitBTC's API
	# Creates instances of the indicators
	# EMA, SMA, BB, RSI, MACD
	api = hitbtc.HitBTC(data["keys"]["public"], data["keys"]["private"])
	timestamp = "[" + strftime("%d %b %Y %H:%M:%S", gmtime()) + "]"
	bb_indicator = bb.BollingerBand(data["indicators"]["bb"]["period"], data["indicators"]["bb"]["multiplier"], None)
	sma_indicator = sma.SimpleMovingAverage(data["indicators"]["sma"]["period"], None)
	ema_indicator = ema.ExponentialMovingAverage(data["indicators"]["ema"]["period"], None)
	rsi_indicator = rsi.RelativeStrengthIndex(data["indicators"]["rsi"]["period"], None)
	macd_indicator = macd.MovingAverageConvergenceDivergence(data["indicators"]["macd"]["fastLength"], data["indicators"]["macd"]["slowLength"], data["indicators"]["macd"]["signalLength"], None)
	print(timestamp + " Apllying indicator settings")

	# Waits for 7 seconds and Clears the console
	os.system("cls")


	# Loops through data_set
	# Iteration starts at index 30 for safety
	for i in data_set[99:]:

		# Variables
		check_list = []		
		current_close = close_data[:epoch_num+100]
		

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
		# Applies restrictor setting
		# Appends current market iteration to opportunity list if a buy occurs
		if check_list.count(1) >= data["restrictor"]["buy"]:
			if not opportunity:
				entered = True
				opportunity = True
				if start_price == 0:
					start_price = float(i["close"])
				else:
					pass
		
		# Checks if the current market iteration is in opportunity list
		if opportunity:

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
			# Remove current market iteration to opportunity list if a sell occurs
			if check_list.count(1) >= data["restrictor"]["sell"]:
				if opportunity:
					trades += 1
					end_price = float(i["close"])
					portfolio = (end_price/start_price) * portfolio
					entered = False
					opportunity = False
					start_price = 0

		# Concatenates information to a string variable
		line = ("Calculating... " + str(epoch_num) + "/" 
			+ str(len(data_set[99:]) - 1) + " ({0:.2f} %)".format(float(epoch_num/(len(data_set[99:]) - 1) * 100)) + 
			" | {0:.2f}".format(portfolio) + " | {0:.2f}".format(float(i["close"])) + " | " + str(entered) + " | " + str(trades))
		

		# Prints current status of the current iteration
		print(line)
		epoch_num += 1


		# Writes current status to a file
		with open('testResult.txt', 'a') as the_file:
   			the_file.write(line + "\n")

	# Print Results
	print("\n\nPorfolio Result: ${0:.2f}".format(portfolio) + "\nNumber of Trades: " + str(trades))