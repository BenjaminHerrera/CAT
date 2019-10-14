# coding=utf-8

"""
rsi.py

Author:        Benjamin Herrera
Date Created:  10 May 2018
Last Modified: 14 August 2019
"""

# Class of RelativeStrengthIndex
class RelativeStrengthIndex(object):
    """
    Relative Strength Index
    """

    def __init__(self, period, data_set):
        """
        Constructor of RelativeStrengthIndex class

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

    def get_losses_and_gains(self):
        """
        Finds losses in candles, appends them to a list, and returns it

        :return: List, list of losses
        """
        # Local Variables
        list_of_losses_and_gains = []
        closed_values = []

        # Iterates through data_values to fond closed values
        for value in self.data_set:
            # Appends closed values to closed_values
            if type(self.data_set) == dict or type(self.data_set[0]) == dict:
                closed_values.append(value['close'])
            else:
                closed_values.append(value)

        # Iterates through close_values and compares close values to see if there's a loss or not
        for i in range(len(closed_values) - 1):
            # Calculates the difference
            difference = float(closed_values[i + 1]) - float(closed_values[i])

            # Appends the loss or gain to list_of_losses_and_gains
            list_of_losses_and_gains.append(difference)

        # Returns list_of_losses_and_gains
        return list_of_losses_and_gains

    def get_average_gain(self):
        """
        Finds the average gains, appends them to a list, and returns it

        :return: List, list of average gains
        """
        # Local variables
        average_gain = 0

        list_of_average_gains = []
        list_of_losses_and_gains = self.get_losses_and_gains()

        # Loops number times and finds the first average gain
        for i in range(self.period):
            # Checks if the element is positive
            if list_of_losses_and_gains[i] > 0:
                # Sums the elements that are greater than 0
                average_gain += abs(list_of_losses_and_gains[i])

        # Calculates the first average gain
        average_gain = average_gain / self.period

        # Appends the first average gain
        list_of_average_gains.append(average_gain)

        # Iterates throughout the remaining elements of the list to find the remaining average gains
        for i in range(len(list_of_losses_and_gains) - self.period):
            # Checks if the element is greater than 0
            if list_of_losses_and_gains[i + self.period] > 0:
                # Calculates the average gain with the current gain
                average_gain = (((average_gain * (self.period - 1)) + abs(list_of_losses_and_gains[i + self.period]))
                                / self.period)

                # Appends calculated average gain to list_of_average_gains
                list_of_average_gains.append(average_gain)

            # Calculates the average gain with a different way if the element is no positive
            else:
                # Calculates the average gain with 0 if there is no current gain
                average_gain = (((average_gain * (self.period - 1)) + 0.0) / self.period)

                # Appends the calculated average gain to list_of_average_gains
                list_of_average_gains.append(average_gain)

        # Returns list_of_average_gains
        return list_of_average_gains

    def get_average_loss(self):
        """
        Finds the average loss, appends it to a list, and returns it

        :return: List, list of average losses
        """
        # Local variables
        average_gain = 0

        list_of_average_gains = []
        list_of_losses_and_gains = self.get_losses_and_gains()

        # Loops number times and finds the first average gain
        for i in range(self.period):
            # Checks if the element is positive
            if list_of_losses_and_gains[i] < 0:
                # Sums the elements that are greater than 0
                average_gain += list_of_losses_and_gains[i]

        # Calculates the first average gain
        average_gain = average_gain / self.period

        # Appends the first average gain
        list_of_average_gains.append(average_gain)

        # Iterates throughout the remaining elements of the list to find the remaining average gains
        for i in range(len(list_of_losses_and_gains) - self.period):
            # Checks if the element is greater than 0
            if list_of_losses_and_gains[i + self.period] < 0:
                # Calculates the average gain with the current gain
                average_gain = (((average_gain * (self.period - 1)) + list_of_losses_and_gains[i + self.period])
                                / self.period)

                # Appends calculated average gain to list_of_average_gains
                list_of_average_gains.append(average_gain)

            # Calculates the average gain with a different way if the element is no positive
            else:
                # Calculates the average gain with 0 if there is no current gain
                average_gain = (((average_gain * (self.period - 1)) + 0.0) / self.period)

                # Appends the calculated average gain to list_of_average_gains
                list_of_average_gains.append(average_gain)

        # Returns list_of_average_gains
        return list_of_average_gains

    def get_relative_strength(self):
        """
        Calculates the relative strength of the RelativeStrengthIndex indicator

        :return: List, list of relative strength values
        """
        # Local variables
        list_of_average_gains = self.get_average_gain()
        list_of_average_losses = self.get_average_loss()

        list_of_relative_strength = []

        # Loops through the list of average losses and gains, calculates the RS,
        # and appends the values to list_of_relative_strength
        for i in range(len(list_of_average_gains)):

            try:
                # Calculates RS
                RS = list_of_average_gains[i] / list_of_average_losses[i]

                # Appends the calculated value to list_of_relative_strength
                list_of_relative_strength.append(abs(RS))

            except:
                pass

        # Returns list_of_relative_strength
        return list_of_relative_strength

    def get_relative_strength_index(self):
        """
        Calculates the relative strength index and appends the values to a list

        :return: List, list of relative strength index values
        """
        # Local variables
        list_of_relative_strength = self.get_relative_strength()

        list_of_relative_strength_index = []

        # Iterates through list_of_relative_strength and appends the calculated value to
        for i in range(len(list_of_relative_strength)):
            # Calculates the relative strength index
            RSI = 100.0 - (100.0 / (1.0 + list_of_relative_strength[i]))

            # Appends the calculated value to list_of_relative_strength_index
            list_of_relative_strength_index.append(RSI)

        # Returns list_of_relative_strength_index
        return list_of_relative_strength_index
