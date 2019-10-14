@echo off
cls
pip3 install -r requirements.txt

python CAT.py 2

:: ================================================================================
:: HOW TO RUN CAT
::
:: In line 6, the batch file will execute the main script for CAT.
:: It will not run with missing or few parameters.
:: In order to run CAT, you must add 1 parameter:
::
:: 	- Param 1: Switces between modes for CAT. Available modes are
::			   Static Loop (0), Single Market Testing (1), and 
::			   Real Time Virtual Testing (2)
::  - Param 2: Only applies if parameter 1 is set to 1. This is 
::			   the file in which the program will analyze for
::			   testing.
::
:: STATIC LOOP:
:: ------------
:: This mode continously loops over and over again showing buy and sell status and
:: the current loop epoch.
::
:: SINGLE MARKET TESTING:
:: ----------------------
:: This mode tests CAT's performance based on a give JSON data set. This
:: useful when you want to test CAT's performance after tweaking the program's
:: settings. It will show the beginning and the resulting portfolio after running
:: through the given dataset.
:: 
:: REAL TIME VIRTUAL TESTING:
:: --------------------------
:: This mode tests CAT's performance with real time market data. This is helpful
:: to see if CAT can run on a 24/7 opertion or for observing the performance of the 
:: program on a real time basis
::

:: Examples:
:: python CAT.py 0
:: python CAT.py 1 test.json
:: python CAT.py 2
::
:: If the program does not show a test base interface, then recheck the parameters.
:: ================================================================================