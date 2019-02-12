# -*- coding: utf-8 -*-
"""
Filename: dynamic_hosts.py
Created on: 12/02/2019
Project name: dynamic_hosts
Author: Carlos Colon
Description: 
Changes:
    06/02/2019     CECR     Initial version
"""

from dynamic_hosts.database import ServersDB

import dynamic_hosts.logger.logger as log


class DynamicHosts:
    _config = None
    _db = None
    _log = log.Logger()

    def __allow_host(self, host_data):
        result = True

        if self._config.verbose > 1:
            self._log.log_verbose("***** Filtering host {} *****".format(host_data['host']))

        if self._config.environment:
            if self._config.verbose > 1:
                self._log.log_verbose("      Evaluating {} == {}".format(self._config.environment, host_data['environment']))

            result &= self._config.environment == host_data['environment']

        if self._config.role:
            if self._config.verbose > 1:
                self._log.log_verbose("      Evaluating {} == {}".format(self._config.role, host_data['role']))

            result &= self._config.role == host_data['role']

        if self._config.location:
            if self._config.verbose > 1:
                self._log.log_verbose("      Evaluating {} == {}".format(self._config.location, host_data['location']))

            result &= self._config.location == host_data['location']

        if self._config.verbose > 1:
            self._log.log_verbose("      Result {}".format(result))

        return result

    def get_list(self):
        hosts = []
        result = dict()
        result['_meta'] = {
            'hostvars': {},
        }

        for record in self._db.get_all():
            if self.__allow_host(record):
                hosts.append(record['host'])

                if 'variables' in record:
                    result['_meta']['hostvars'][record['host']] = record['variables']

        result['all'] = {
            'hosts': hosts,
            'vars': {}
        }

        if self._config.verbose > 0:
            self._log.log_verbose("After filtering, {} servers were returned".format(str(len(hosts))))

        return result

    def __init__(self, config):
        self._config = config

        self._db = ServersDB(self._config)

        if self._config.verbose > 0:
            self._log.log_verbose("----- Dynamic hosts configuration -----")
            self._log.log_verbose(" Client.......: {}".format(self._config.client))
            self._log.log_verbose(" Environment..: {}".format(self._config.environment))
            self._log.log_verbose(" Role.........: {}".format(self._config.role))
            self._log.log_verbose(" Location.....: {}".format(self._config.location))
