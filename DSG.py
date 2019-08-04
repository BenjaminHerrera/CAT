# coding-utf-8

"""
Author: Benjamin Herrera
Date Created: 3 August 2019
Date Changed: 3 August 2019
"""

# Imports
import sys 
import json
from src.api import hitbtc

# Runs the script
if __name__ == '__main__':\

	# Reads config file
	with open('config.json') as file:
		config = json.load(file)


	# Establishes connection to HitBTC
	conn = hitbtc.HitBTC(config["keys"]["public"], config["keys"]["private"])


	# Writes market data to a json file
	with open('data/' + str(sys.argv[1]) + '.json' , 'w') as file:
		json.dump(conn.get_candles(sys.argv[2], sys.argv[3], limit=(int(sys.argv[4]))), file, indent=2)

