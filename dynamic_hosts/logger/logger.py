# -*- coding: utf-8 -*-
"""
Filename: logger.py
Created on: 07/02/2019
Project name: dynamic_hosts
Author: Carlos Colon
Description: 
Changes:
    06/02/2019     CECR     Initial version
"""


class Logger:
    """Terminal event logger

    This object allows you to display event information in the console.
    """

    _line = '''%s[%s%s%s]%s %s'''

    class __Colors:
        Reset = '\033[0m'
        Bold = '\033[01m'
        Underline = '\033[04m'
        StrikeThrough = '\033[09m'

        class FG:
            Black = '\033[30m'

            Cyan = '\033[36m'
            LightCyan = '\033[96m'

            Red = '\033[31m'
            LightRed = '\033[91m'

            Green = '\033[32m'
            LightGreen = '\033[92m'

            Blue = '\033[34m'
            LightBlue = '\033[94m'

            Yellow = '\033[93m'

        class BG:
            Black = '\033[40m'
            Green = '\033[42m'
            Blue = '\033[44m'

    @property
    def get_colors(self):
        return self.__Colors

    def log_error(self, message):
        """Displays a formatted error line with a message in the terminal.

        :param message: The message that will be shown
        :return: None
        """
        line = self._line % (self.__Colors.Reset,
                             self.__Colors.FG.Red,
                             " ERROR ",
                             self.__Colors.Reset,
                             self.__Colors.FG.LightRed,
                             message)

        print(line)

    def log_warning(self, message):
        """Displays a formatted warning line with a message in the terminal.

        :param message: The message that will be shown
        :return: None
        """
        line = self._line % (self.__Colors.Reset,
                             self.__Colors.FG.Yellow,
                             "WARNING",
                             self.__Colors.Reset,
                             self.__Colors.FG.Yellow,
                             message)

        print(line)

    def log_info(self, message):
        """Displays a formatted information line with a message in the terminal.

        :param message: The message that will be shown
        :return: None
        """
        line = self._line % (self.__Colors.Reset,
                             self.__Colors.FG.Blue,
                             " INFO  ",
                             self.__Colors.Reset,
                             self.__Colors.Reset,
                             message)

        print(line)

    def log_verbose(self, message):
        """Displays a formatted verbose line with a message in the terminal.

        :param message: The message that will be shown
        :return: None
        """
        line = self._line % (self.__Colors.Reset,
                             self.__Colors.FG.Green,
                             "VERBOSE",
                             self.__Colors.Reset,
                             self.__Colors.FG.LightGreen,
                             message)

        print(line)
