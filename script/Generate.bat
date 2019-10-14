@echo off
pip3 install -r requirements.txt

python DSG.py test BTCUSD M30 1000

:: ================================================================================
:: HOW TO MAKE A DATA SET
:: 
:: In line 6, the batch file will execute the data set generator script.
:: It will not run with missing or few parameters.
:: In order to make a data set, you must add 4 parameters:
::
:: 	- Param 1: Name of the data set file
:: 	- Param 2: The market of the data set file
::  - Param 3: The time period
::  - Param 4: The number of candles in the data set file
::
:: Examples:
:: python DSG.py dataSetOne BTCUSD M15 100	
:: python DSG.py result ETHBTC H1 250
:: python DSG.py test LTCETH D1 500
::
:: Once the batch file is executed, the resulting data set will be created
:: at the "data" directory. Contents will be stored in JSON format and the
:: data set will be a JSON file	
::
:: If a data set could not be formed, check the parameters on line 6 of this file.
:: ================================================================================