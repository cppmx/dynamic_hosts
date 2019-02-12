# -*- coding: utf-8 -*-
"""
Filename: database
Created on: 08/02/2019
Project name: dynamic_hosts
Author: Carlos Colon
Description: 
Changes:
    06/02/2019     CECR     Initial version
"""

import os
import json
import jsonschema
import dynamic_hosts.logger.logger as log


def _request_data(field):
    """This function requests a data in the terminal

    :param field: The name of the field that will receive the data
    :return: The data that the user has typed
    """
    message = ' - {:.<20}: '.format(field.capitalize())
    result = input(message)

    return result


class Server:
    """Object that represents a Server

    This object will be used as a data model of the database
    """

    _schema = {}
    _server = {}
    _logger = log.Logger()

    def __schema_validation(self, data):
        result = True

        try:
            v = jsonschema.Draft4Validator(self._schema)
            for error in sorted(v.iter_errors(data), key=str):
                self._logger.log_error(error)
                result = False
        except jsonschema.ValidationError as e:
            self._logger.log_error(e.message)
            result = False

        return result

    def __validate(self, data=None):
        if data:
            return self.__schema_validation(data)
        else:
            return self.__schema_validation(self._server)

    def get_data(self):
        """Returns server data

        :return: Returns a dictionary with the server data
        """
        return self._server

    def is_equal(self, data):
        result = True

        for f in self._schema['required']:
            result &= data[f] == self._server[f]

        return result

    def add_field(self, field, value):
        self._server[field] = value

        return self.__validate()

    def __init__(self, data):
        """Object constructor

        :param data: A dictionary with the data of the new object
        """

        '''Loads the db data'''
        _server_schema_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db", "record.schema.json")
        if os.path.isfile(_server_schema_file):
            with open(_server_schema_file) as f:
                self._schema = json.load(f)

        if not data:
            for f in self._schema['required']:
                value = _request_data(f)

                if not value:
                    raise Exception("Field \'{}\' is required and a blank value was obtained".format(f))

                self._server[f] = value
        else:
            if not self.__validate(data):
                raise Exception("Invalid data")
            else:
                self._server = data


class ServersDB:
    """Object that manages the functions of the database"""

    _db_file = ''
    _config = None
    _log = log.Logger()
    _schema = {}
    _servers = []

    def __validate_db(self):
        """Validate the database information against the schema"""
        result = True

        try:
            v = jsonschema.Draft4Validator(self._schema)
            for error in sorted(v.iter_errors(self._servers), key=str):
                if self._config.verbose > 0:
                    self._log.log_error(error)
                result = False
        except jsonschema.ValidationError as e:
            if self._config.verbose > 0:
                self._log.log_error(e.message)
            result = False

        return result

    def __save(self):
        """Save changes on the DB

        :return: True if the information to be stored meets the requirements of the schema,
                 otherwise an exception will be thrown.
        """

        result = self.__validate_db()

        if result:
            with open(self._db_file, 'w') as outfile:
                json.dump(self._servers, outfile)
        else:
            if self._config.verbose > 0:
                self._log.log_verbose("Failure to save the data, check the structure of the database")

            raise Exception("Something went wrong")

        return result

    def __request_vars_data(self):
        """Private function to request variable information"""
        if self._config.verbose > 0:
            self._log.log_verbose("Requesting variable information")

        add_vars = input("Do you want to add variables for this host (y/N)? ")
        result = {}

        while add_vars == 'y' or add_vars == 'Y':
            var_name = input("Variable name: ")

            if not var_name.strip():
                self._log.log_warning("Variable name cannot be empty, try again")
                continue

            var_data = input("Value for \"" + var_name + "\" variable: ")

            if not var_name.strip():
                self._log.log_warning("Variable value cannot be empty, try again")
                continue

            result[var_name] = var_data

            add_vars = input("Do you want to add another variable for this host (y/N)? ")

        return result

    def add_new_server(self, server_data=None, allow_host_vars=False):
        """This function adds a new record to the DB

        :param server_data: A Server instance
        :param allow_host_vars: Specifies whether variables are allowed per host
        :return: None
        """

        if self._config.verbose > 0:
            self._log.log_verbose("Adding new server")

        if server_data is None:
            server_data = Server(server_data)

        for entry in self._servers:
            if server_data.is_equal(entry):
                if self._config.verbose > 0:
                    self._log.log_verbose("Duplicate value: {}".format(json.dumps(entry)))

                raise Exception("Duplicated data")

        if allow_host_vars:
            host_vars = self.__request_vars_data()

            if len(host_vars) > 0:
                server_data.add_field('variables', host_vars)

        self._servers.append(server_data.get_data())

        self.__save()

    def update_server(self, new_server_data):
        """This function updates information of a server

        :param new_server_data: A Server instance
        :return: None
        """

        if self._config.verbose > 0:
            self._log.log_verbose("Updating server information")

        result = False

        for entry in self._servers:
            if new_server_data.is_equal(entry):
                entry = new_server_data.get_data()

                if self._config.verbose > 0:
                    self._log.log_verbose("New Server data: " + entry.get_data())

                result = self.__save()

                break

        return result

    def delete_server(self, server_data):
        """This function deletes a record from the DB

        :param server_data: A Server instance
        :return: None
        """

        if self._config.verbose > 0:
            self._log.log_verbose("Deleting server data from DB")

        result = False
        idx = 0

        for entry in self._servers:
            if server_data.is_equal(entry):
                del self._servers[idx]

                result = self.__save()

                break

            idx += 1

        return result

    def get_servers(self, field_name, field_value, _all=False):
        """Returns a server based on the criteria of the parameters

        To find a server in the database, a search criteria is required.

        The search criterion refers to a field and its value.

        :param field_name: Field name
        :param field_value: Field's value
        :param _all: This flag determines whether all records that match the search criteria
                    or only the first match are returned.
        :return: None if the criterion was not met, otherwise a Server instance
        """

        if self._config.verbose > 0:
            self._log.log_verbose("Searching for a specific record")

        result = []

        for entry in self._servers:
            if entry[field_name] == field_value:
                result.append(Server(entry))
                if not _all:
                    break

        if self._config.verbose > 0 and not result:
            self._log.log_verbose("No record found - Filter: ({} == {})".format(field_name, field_value))

        return result

    def get_all(self):
        """Returns all servers as JSON

        :return: A JSON like data
        """

        if self._config.verbose > 0:
            self._log.log_verbose("Getting all servers")

        return self._servers

    def __init__(self, configuration):
        """ServerDB constructor

        :param client: A Client name
        :param configuration: A configuration instance
        """

        self._config = configuration

        """Load the DB schema file"""
        _db_schema_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db", "db.schema.json")
        if os.path.isfile(_db_schema_file):
            with open(_db_schema_file) as f:
                self._schema = json.load(f)

        """Check if there is a folder for this client, if not then create a new one"""
        if not os.path.isdir(os.path.join(self._config.servers_folder, self._config.client)):
            if self._config.verbose > 0:
                self._log.log_verbose("There is no folder for this client, creating new one")

            os.makedirs(os.path.join(self._config.servers_folder, self._config.client), 755)

        """Check if there is a DB file for this client, if so then load and validate the data"""
        self._db_file = self._config.get_db_file(self._config.client)

        if os.path.isfile(self._db_file):
            with open(self._db_file) as f:
                self._servers = json.load(f)

        if self._servers and not self.__validate_db():
            raise Exception("There is a corruption in the database")
