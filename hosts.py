# -*- coding: utf-8 -*-
"""
Filename: hosts.py
Created on: 07/02/2019
Project name: dynamic_hosts
Author: Carlos Colon
Description: 
Changes:
    06/02/2019     CECR     Initial version
"""

from dynamic_hosts import configuration

import argparse
import unittest

_configuration = configuration.ProdConfig()


def show_config():
    message = ' - {:.<20}: {}'
    print("***** D Y N A M I C   H O S T S *****")
    print("            CONFIGURATION")
    print("*************************************")
    print(message.format("Client", _configuration.client))
    print(message.format("Environment", _configuration.environment))
    print(message.format("Role", _configuration.role))
    print(message.format("Location", _configuration.location))
    print("*************************************")


def test():
    """Runs the tests"""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')

    result = unittest.TextTestRunner(verbosity=2).run(tests)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dynamic host generating tool')
    parser.add_argument('--config', action='store_true', help='Display current configuration')
    parser.add_argument('--env', choices=['dev', 'test', 'prod'],
                        help='Execution environment of this script. By default it is executed in production.')
    parser.add_argument('--list', action='store_true',
                        help='Returns all hosts that meet the criteria.')
    parser.add_argument('--new-server', action='store_true', help='Add new server record.')
    parser.add_argument('--test', action='store_true', help='Run tests')
    parser.add_argument('--update-server', action='store_true', help='Update information of a server.')
    parser.add_argument('--verbose', '-v', action='count',
                        help='Displays extra data in the console output. It should not be used in production.')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    if args.env:
        if args.env == 'dev':
            _configuration = configuration.DevConfig()
        elif args.env == 'test':
            _configuration = configuration.TestConfig()

    if args.test:
        exit(test())

    if args.config:
        show_config()

