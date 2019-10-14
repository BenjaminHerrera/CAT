# coding=utf-8

"""
sma.py

Author:        Benjamin Joseph Lucero Herrera
Date Created:  18 May 2018
Last Modified: 14 August 2019
"""

# Class of SimpleMovingAverage
class SimpleMovingAverage(object):
    """
    Simple Moving Average
    """

    def __init__(self, period, data_set):
        """
        Constructor of SimpleMovingAverage class

        :param period: Integer, integer used to calculate RelativeStrengthIndex
        :param data_set: Dict or List, a set of data to parse
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

    def get_sma(self):
        """5
        Calculates the SimpleMovingAverage

        :return: List, list of SimpleMovingAverage at different times
        """
        # Local Variables
        closed_values = []
        list_of_sma_values = []


        # Tries to parse data_set
        try:
            # Iterates through data_values to fond closed values
            for value in self.data_set:
                # Appends closed values to closed_values
                if type(self.data_set) == dict or type(self.data_set[0]) == dict:
                    closed_values.append(value["close"])
                else:
                    closed_values.append(value)

        # If an error is found, the function will pass the value from data_set to closed_values
        except TypeError:
            # Copies values to closed_values
            closed_values = self.data_set

        # Iterates through close_values, calculates SimpleMovingAverage, and appends the values to list_of_sma_values
        for i in range(len(closed_values) - self.period + 1):
            # Resets sum_of_values
            sum_of_values = 0

            # Iterates again to sum up number of close values
            for j in range(self.period):
                # Sums up a number of closed values
                sum_of_values += float(closed_values[i + j])

            # Divides sum_of_values to get SimpleMovingAverage
            sum_of_values = sum_of_values / self.period

            # Appends value to list_of_sma_values
            list_of_sma_values.append(sum_of_values)

        # Returns list_of_sma_values
        return list_of_sma_values
