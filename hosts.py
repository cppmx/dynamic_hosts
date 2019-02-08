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

from dynamic_hosts.logger import logger

if __name__ == "__main__":
    log = logger.Logger()

    log.log_info("Test")
    log.log_error("Test")
    log.log_warning("Test")
    log.log_verbose("Test")

