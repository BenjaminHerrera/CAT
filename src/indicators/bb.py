# coding=utf-8

"""
bb.py

Author:        Benjamin Herrera
Date Created:  20 May 2018
Last Modified: 14 August 2019
"""

# Imports
from src.indicators import sma


# Class of BollingerBand
class BollingerBand(object):
    """
    Bollinger Bands
    """

    def __init__(self, period, multiplier, data_set):
        """
        Constructor of BollingerBand class

        :param period: Integer, integer used to calculate ExponentialMovingAverage
        :param multiplier: Float, float used to determine to width of the bands
        :param data_set: Dict or List, used to parse information
        """
        self.period = period
        self.multiplier = multiplier
        self.data_set = data_set

    def set_data_set(self, data_set):
        """
        Changes value of data_set

        :param data_set: Dict or List, used to parse information
        self.data_set = data_set
        """
        self.data_set = data_set

    def get_middle_band(self):
        """
        Calculates the middle band of the indicator

        :return: List, list of middle band values
        """
        # Local variable
        sma_01 = sma.SimpleMovingAverage(self.period, self.data_set)

        # Returns a 20 day SimpleMovingAverage
        return sma_01.get_sma()

    def get_upper_band(self):
        """
        Calculates the upper band of the indicator

        :return: List, list of upper band values
        """
        # Local variables
        list_of_SMA_values = self.get_middle_band()

        closed_values = []
        list_of_upper_band_values = []

        # Iterates through data_values to fond closed values
        for value in self.data_set:
            # Appends closed values to closed_values
            if type(self.data_set) == dict:
                closed_values.append(value['close'])
            else:
                 closed_values.append(value)

        # Iterates through the SimpleMovingAverage
        for i in range(len(closed_values) - self.period + 1):
            # Resets variables
            standard_deviation = 0
            mean = 0

            # Finds the mean of part of the list
            for j in range(self.period):
                # Adds the elements together
                mean += float(closed_values[i + j])

            # Calculates the mean
            mean = mean / self.period

            # Iterates again to find th deviations
            for j in range(self.period):
                # Calculates the deviance
                deviance = (float(closed_values[i + j]) - mean) ** self.multiplier

                # Sums up the deviance
                standard_deviation = standard_deviation + deviance

            # Calculates the mean of deviance
            standard_deviation = standard_deviation / self.period

            # Calculates standard deviance
            standard_deviation **= 0.5

            # Calculates and appends the value of the upper band of the indicator
            list_of_upper_band_values.append(list_of_SMA_values[i] + (standard_deviation * 2))

        # Returns list_of_upper_band_values
        return list_of_upper_band_values

    def get_lower_band(self):
        """
        Calculates the upper band of the indicator

        :return: List, list of upper band values
        """
        # Local variables
        list_of_SMA_values = self.get_middle_band()

        closed_values = []
        list_of_upper_band_values = []

        # Iterates through data_values to fond closed values
        for value in self.data_set:
            # Appends closed values to closed_values
            if type(self.data_set) == dict or type(self.data_set[0]) == dict:
                closed_values.append(value['close'])
            else:
                closed_values.append(value)

        # Iterates through the SimpleMovingAverage
        for i in range(len(closed_values) - self.period + 1):
            # Resets variables
            standard_deviation = 0
            mean = 0

            # Finds the mean of part of the list
            for j in range(self.period):
                # Adds the elements together
                mean += float(closed_values[i + j])

            # Calculates the mean
            mean = mean / self.period

            # Iterates again to find th deviations
            for j in range(self.period):
                # Calculates the deviance
                deviance = (float(closed_values[i + j]) - mean) ** self.multiplier

                # Sums up the deviance
                standard_deviation = standard_deviation + deviance

            # Calculates the mean of deviance
            standard_deviation = standard_deviation / self.period

            # Calculates standard deviance
            standard_deviation **= 0.5

            # Calculates and appends the value of the upper band of the indicator
            list_of_upper_band_values.append(list_of_SMA_values[i] - (standard_deviation * 2))

        # Returns list_of_upper_band_values
        return list_of_upper_band_values
