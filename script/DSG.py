# coding-utf-8

"""
Author: Benjamin Herrera
Date Created: 3 August 2019
Date Changed: 13 October 2019
"""

# Imports
import sys 
import json
import os

# Changes the searching scope
sys.path.insert(1, os.path.dirname(os.path.realpath("")))

# Import hitbtc
from src.api import hitbtc


# Runs the script
if __name__ == '__main__':\

	# Reads config file
	with open(os.path.dirname(os.path.realpath("")) + '\\config.json') as file:
		config = json.load(file)

	# Establishes connection to HitBTC
	conn = hitbtc.HitBTC(config["keys"]["public"], config["keys"]["private"])

	# Writes market data to a json file
	with open(os.path.dirname(os.path.realpath("")) + '\\data\\' + str(sys.argv[1]) + '.json' , 'w') as file:
		json.dump(conn.get_candles(sys.argv[2], sys.argv[3], limit=(int(sys.argv[4]))), file, indent=2)

	print("DSG >> " + str(sys.argv[1]) + ".json Generation\033[32m Complete \033[0m")