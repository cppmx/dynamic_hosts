# -*- coding: utf-8 -*-
"""
Filename: test_logger
Created on: 07/02/2019
Project name: dynamic_hosts
Author: Carlos Colon
Description: 
Changes:
    06/02/2019     CECR     Initial version
"""

from dynamic_hosts.logger import logger
from tests.console import read_console

import json
import unittest


class TestLogger(unittest.TestCase):
    _colors = {
        "Reset": "\033[0m",
        "Bold": "\033[01m",
        "Underline": "\033[04m",
        "StrikeThrough": "\033[09m",
        "FG_Black": "\033[30m",
        "FG_Cyan": "\033[36m",
        "FG_LightCyan": "\033[96m",
        "FG_Red": "\033[31m",
        "FG_LightRed": "\033[91m",
        "FG_Green": "\033[32m",
        "FG_LightGreen": "\033[92m",
        "FG_Blue": "\033[34m",
        "FG_LightBlue": "\033[94m",
        "FG_Yellow": "\033[93m",
        "BG_Black": "\033[40m",
        "BG_Green": "\033[42m",
        "BG_Blue": "\033[44m"
    }

    _logger = None
    _test_words = ''

    def setUp(self):
        self._logger = logger.Logger()

        with open("words.json") as f:
            self._test_words = json.load(f)

    def test_colors(self):
        self.assertEqual(self._colors['Reset'], self._logger.get_colors.Reset, "Wrong color")
        self.assertEqual(self._colors['Bold'], self._logger.get_colors.Bold, "Wrong color")
        self.assertEqual(self._colors['Underline'], self._logger.get_colors.Underline, "Wrong color")
        self.assertEqual(self._colors['StrikeThrough'], self._logger.get_colors.StrikeThrough, "Wrong color")
        self.assertEqual(self._colors['FG_Black'], self._logger.get_colors.FG.Black, "Wrong color")
        self.assertEqual(self._colors['FG_Cyan'], self._logger.get_colors.FG.Cyan, "Wrong color")
        self.assertEqual(self._colors['FG_LightCyan'], self._logger.get_colors.FG.LightCyan, "Wrong color")
        self.assertEqual(self._colors['FG_Red'], self._logger.get_colors.FG.Red, "Wrong color")
        self.assertEqual(self._colors['FG_LightRed'], self._logger.get_colors.FG.LightRed, "Wrong color")
        self.assertEqual(self._colors['FG_Green'], self._logger.get_colors.FG.Green, "Wrong color")
        self.assertEqual(self._colors['FG_LightGreen'], self._logger.get_colors.FG.LightGreen, "Wrong color")
        self.assertEqual(self._colors['FG_Blue'], self._logger.get_colors.FG.Blue, "Wrong color")
        self.assertEqual(self._colors['FG_LightBlue'], self._logger.get_colors.FG.LightBlue, "Wrong color")
        self.assertEqual(self._colors['FG_Yellow'], self._logger.get_colors.FG.Yellow, "Wrong color")
        self.assertEqual(self._colors['BG_Black'], self._logger.get_colors.BG.Black, "Wrong color")
        self.assertEqual(self._colors['BG_Green'], self._logger.get_colors.BG.Green, "Wrong color")
        self.assertEqual(self._colors['BG_Blue'], self._logger.get_colors.BG.Blue, "Wrong color")

    def test_error_messages(self):
        for word in self._test_words:
            expected_output = '\x1b[0m[\x1b[31m ERROR \x1b[0m]\x1b[91m %s\n' % word

            with read_console(self._logger.log_error, word) as output:
                self.assertEqual(expected_output, output)

    def test_info_messages(self):
        for word in self._test_words:
            expected_output = '\x1b[0m[\x1b[34m INFO  \x1b[0m]\x1b[0m %s\n' % word

            with read_console(self._logger.log_info, word) as output:
                self.assertEqual(expected_output, output)

    def test_warn_messages(self):
        for word in self._test_words:
            expected_output = '\x1b[0m[\x1b[93mWARNING\x1b[0m]\x1b[93m %s\n' % word

            with read_console(self._logger.log_warning, word) as output:
                self.assertEqual(expected_output, output)

    def test_verbose_messages(self):
        for word in self._test_words:
            expected_output = '\x1b[0m[\x1b[32mVERBOSE\x1b[0m]\x1b[92m %s\n' % word

            with read_console(self._logger.log_verbose, word) as output:
                self.assertEqual(expected_output, output)


if __name__ == '__main__':
    unittest.main()
