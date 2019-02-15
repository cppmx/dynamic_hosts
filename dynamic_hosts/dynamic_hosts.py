# -*- coding: utf-8 -*-
"""dynamic_hosts.py
====================================
Created on: 09/02/2019
@author Carlos Colón
"""

from dynamic_hosts.database import ServersDB

import dynamic_hosts.logger.logger as log


class DynamicHosts:
    """Dynamic Hosts class

    This object is responsible for assembling the list of hosts in a format understandable to Ansible.

    It maintains a single instance to the database to request different actions.

    This class has the following attributes:

    Attributes:
        _config (Config): An instance of an object based on Config
        _db (ServersDB): An instance to the database
        _log (Logger): An instance to the event logger object

    All these attributes are private and can not be modified once an instance of this class is created.
    """

    _config = None
    _db = None
    _log = log.Logger()

    @property
    def get_client(self):
        """Returns the name of the client of the active configuration"""
        return self._config.client

    @property
    def get_environment(self):
        """Returns the environment value of the active configuration"""
        return self._config.environment

    @property
    def get_role(self):
        """Returns the role value of the active configuration"""
        return self._config.role

    @property
    def get_location(self):
        """Returns the location value of the active configuration"""
        return self._config.location

    def __allow_host(self, host_data):
        """A private help function

        This function receives a dictionary with information about a specific host,
        and with that information it makes an analysis to determine if this host
        should be included or not in the final list.

        :param host_data: A host's data dictionary
        :return: True if the host is validated by the filters, otherwise False
        """
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
        """Get List function

        This function returns a list of hosts in a format that can be used by Ansible.

        :return: An Ansible host's inventory in JSON format
        """
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

    def add_server(self):
        """Trivial function that notifies the database that the user wants to add a new record

        :return: 0 if the insertion of the new record was successful, otherwise 1
        """
        result = 0

        try:
            self._db.add_new_server(server_data=None, allow_host_vars=True)
        except Exception as ex:
            self._log.log_error(ex)

            result = 1

        return result

    def update_server(self):
        """Trivial function that notifies the database that the user wants to modify a record

        :return: 0 if the update of the record was successful, otherwise 1
        """
        result = 0

        try:
            self._db.update_server(new_server_data=None)
        except Exception as ex:
            self._log.log_error(ex)

            result = 1

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
