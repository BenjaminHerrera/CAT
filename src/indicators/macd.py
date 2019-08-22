# coding=utf-8

"""
macd.py

Author:        Benjamin Joseph Lucero Herrera
Date Created:  26 April 2018
Last Modified: 12 August 2019
"""

# Import
from src.indicators import ema
from src.indicators import sma


# Class of MovingAverageConvergenceDivergence
class MovingAverageConvergenceDivergence(object):
    """
    Moving Average Convergence Divergence
    """

    def __init__(self, fast_length_time_period, slow_length_time_period, signal_time_period, data_set):
        """
        Constructor of MovingAverageConvergenceDivergence class
    
        :param fast_length_time_period: Integer, integer used to calculate ExponentialMovingAverage for fast length
        :param slow_length_time_period: Integer, integer used to calculate ExponentialMovingAverage for slow length
        :param signal_time_period: Integer, integer used to calculate ExponentialMovingAverage for signal
        :param data_set: Dict of List, a set of data to parse
        """
        self.data_set = data_set
        self.signal_time_period = signal_time_period
        self.fast_length_time_period = fast_length_time_period
        self.slow_length_time_period = slow_length_time_period

    def set_data_set(self, data_set):
        """
        Changes value of data_set

        :param data_set: Dict or List, used to parse information
        self.data_set = data_set
        """
        self.data_set = data_set

    def get_ema_of_fast_length(self):
        """
        Returns EMA of fast length

        :return: List, EMA of fast length
        """
        # Local Variable
        ema_fast_length = ema.ExponentialMovingAverage(self.fast_length_time_period, self.data_set)

        # Returns ExponentialMovingAverage Value
        return ema_fast_length.get_ema()

    def get_ema_of_slow_length(self):
        """
        Returns EMA of slow length

        :return: List, EMA of slow length
        """
        # Local Variable
        ema_slow_length = ema.ExponentialMovingAverage(self.slow_length_time_period, self.data_set)

        # Returns ExponentialMovingAverage value
        return ema_slow_length.get_ema()

    def get_macd(self):
        """
        Returns the difference between the slow length EMA and the fast length EMA, MACD

        :return: List, EMA of MACD
        """
        # Local Variables
        list_of_slow_length_values = self.get_ema_of_slow_length()
        list_of_fast_length_values = self.get_ema_of_fast_length()

        list_of_macd_values = []

        # Iterates to find individual ExponentialMovingAverage Values
        for i in range(len(list_of_slow_length_values)):
            # Find Difference
            difference = list_of_fast_length_values[i + (self.slow_length_time_period - self.fast_length_time_period)] - list_of_slow_length_values[i]

            # Appends value to list_of_macd_values
            list_of_macd_values.append(difference)

        # Returns list_of_macd_values
        return list_of_macd_values

    def get_sma_of_signal(self):
        """
        Returns the EMA of the signal, EMA of MACD

        :return: List of signal ExponentialMovingAverage values
        """
        # Local Variable
        sma_of_signal = sma.SimpleMovingAverage(self.signal_time_period, self.get_macd())

        # Returns the ExponentialMovingAverage
        return sma_of_signal.get_sma()

    def get_histogram_data(self):
        """
        Returns the difference between MACD EMA and Signal EMA

        :return: List of differences
        """
        # Local Variables
        list_of_MACD_values = self.get_macd()
        list_of_signal_SMA = self.get_sma_of_signal()

        list_of_differences = []

        # Iterates to find the difference between MACD EMA and Signal EMA
        for i in range(len(list_of_signal_SMA)):
            # Finds the difference
            difference = list_of_MACD_values[i + self.signal_time_period - 1] - list_of_signal_SMA[i]

            # Appends the difference to a list
            list_of_differences.append(difference)

        # Returns the Histogram Data
        return list_of_differences
