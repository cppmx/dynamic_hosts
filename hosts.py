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

import argparse


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

