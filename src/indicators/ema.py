# coding=utf-8

"""
ema.py

Author:        Benjamin Joseph Lucero Herrera
Date Created:  26 April 2018
Last Modified: 26 March 2019
"""

# Imports
from src.indicators import sma


# Class of ExponentialMovingAverage
class ExponentialMovingAverage(object):
    """
    Exponential Moving Average
    """

    def __init__(self, period, data_set):
        """
        Constructor of ExponentialMovingAverage class

        :param period: Integer, integer used to calculate ExponentialMovingAverage
        :param data_set_dict: Dict, a set of data to parse
        :param data_set: Dict of List, a set of data to parse
        """
        self.period = period
        self.data_set = data_set

    def set_data_set(self, data_set):
        """
        Changes value of data_set

        :param data_set: Dict or List, used to parse information
        self.data_set = data_set
        """
        self.data_set = data_set


    def get_ema(self):
        """
        calculates the ExponentialMovingAverage

        :return: List, list of ExponentialMovingAverage values at different times
        """
        # Local variables
        weighted_variable = 2 / (self.period + 1.0)

        closed_values = []
        list_of_ema_values = []

        # Passes the data_set to the list parameter
        sma_01 = sma.SimpleMovingAverage(self.period, self.data_set)

        
        for value in self.data_set:
            # Appends closed values to closed_values
            closed_values.append(value["close"])

        # Calculates the first ExponentialMovingAverage value
        EMA_value = sma_01.get_sma()[0]

        # Appends the first ExponentialMovingAverage value to list_of_ema_values
        list_of_ema_values.append(EMA_value)

        # Calculates the ExponentialMovingAverage of the other candles
        for i in range(len(closed_values) - self.period):
            # Calculates ExponentialMovingAverage for individual candle
            EMA_value = EMA_value + weighted_variable * (float(closed_values[i + self.period]) - EMA_value)

            # Appends calculated ExponentialMovingAverage to list_of_ema_values
            list_of_ema_values.append(EMA_value)

        # Returns the list
        return list_of_ema_values