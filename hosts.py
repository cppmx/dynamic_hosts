#!/usr/bin/env python3
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

try:
    import dynamic_hosts._version as _V_
    from dynamic_hosts import configuration
    from dynamic_hosts import dynamic_hosts
except ImportError:
    print("The script has not found the necessary dependencies and will be closed.")
    print("Please execute the installation command: 'python setup.py install'")
    exit(2)

import json
import argparse
import unittest

_configuration = configuration.ProdConfig()
_dyn_hosts = None


def show_config():
    success = 0

    message = ' - {:.<20}: {}'
    print("***** D Y N A M I C   H O S T S *****")
    print("            CONFIGURATION")
    print("*************************************")
    print(message.format("Client", _configuration.client))
    print(message.format("Environment", _configuration.environment))
    print(message.format("Role", _configuration.role))
    print(message.format("Location", _configuration.location))
    if _configuration.verbose > 0:
        print(message.format("Database", _configuration.get_db_file()))
    print("*************************************")

    return success


def test():
    """Runs the tests"""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')

    result = unittest.TextTestRunner(verbosity=2).run(tests)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dynamic host generating tool')
    parser.add_argument('--client', type=str, help='A valid client')
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
    parser.add_argument('--version', action='version', version='%(prog)s {} build {}'.format(_V_.__version__, _V_.__build__))

    args = parser.parse_args()

    if args.env:
        if args.env == 'dev':
            _configuration = configuration.DevConfig()
        elif args.env == 'test':
            _configuration = configuration.TestConfig()

    if args.verbose:
        _configuration.verbose = args.verbose

    if args.test:
        exit(test())

    if args.client:
        _configuration.client = args.client

    if args.config:
        exit(show_config())

    _dyn_hosts = dynamic_hosts.DynamicHosts(_configuration)

    if args.new_server:
        print("Please enter the following information:")
        exit(_dyn_hosts.add_server())

    if args.update_server:
        print("Please enter the following information:")
        exit(_dyn_hosts.update_server())

    if args.list:
        data = _dyn_hosts.get_list()

        if _configuration.verbose > 0:
            print(json.dumps(data, indent=4, sort_keys=True))
        else:
            print(json.dumps(data))
