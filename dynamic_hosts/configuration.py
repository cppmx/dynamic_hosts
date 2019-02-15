# -*- coding: utf-8 -*-
"""configuration.py
====================================
Created on: 07/02/2019
@author Carlos Colón
"""

import os


class Config:
    """Configuration base class

    All possible configurations will use this object as a base, inheriting the following private attributes:

    Attributes:
        _client (str): The client's name
        _environment (str): This attribute is used to perform searches in the database.
                            Sets the value of the ambient field.
        _group (str): This attribute is used to perform searches in the database.
                      Sets the value of the group field.
        _location (str): This attribute is used to perform searches in the database.
                         Sets the value of the location field.
        _servers_folder (str): The absolute path where the database will be stored.
        _servers_file (str): The name of the database file.
        _verbose (int): The verbosity level

    For each of these attributes, a property has been created to obtain its value or establish a new value.
    """

    _verbose = 0

    _client = ''
    _environment = ''
    _group = ''
    _role = ''
    _location = ''

    _servers_folder = ''
    _servers_file = ''

    @property
    def servers_folder(self):
        """Returns the absolute path of the DB's folder"""
        return os.path.abspath(self._servers_folder)

    @property
    def servers_file(self):
        """Returns the server's file name"""
        return self._servers_file

    @property
    def verbose(self):
        """Returns the verbosity log level"""
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        """sets the verbosity log level"""
        if value:
            self._verbose = value

    @property
    def client(self):
        """Returns the client name"""
        return self._client

    @client.setter
    def client(self, value):
        """Sets the client name"""
        if value:
            self._client = value

    @property
    def environment(self):
        """Returns the value of the environment variable"""
        return self._environment

    @environment.setter
    def environment(self, value):
        """Sets the value of the environment variable"""
        self._environment = value

    @property
    def group(self):
        """Returns the value of the group variable"""
        return self._group

    @group.setter
    def group(self, value):
        """Sets the value of the group variable"""
        self._group = value

    @property
    def role(self):
        """Returns the value of the role variable"""
        return self._role

    @role.setter
    def role(self, value):
        """Sets the value of the role variable"""
        self._role = value

    @property
    def location(self):
        """Returns the value of the location variable"""
        return self._location

    @location.setter
    def location(self, value):
        """Sets the value of the location variable"""
        self._location = value

    def get_db_file(self):
        """Returns the absolute path to the database file"""
        return os.path.abspath(os.path.join(self._servers_folder, self._client, self._servers_file))


class DevConfig(Config):
    """Development Configuration class

    This class inherits the attributes of the Config class.
    """
    def __init__(self):
        self.verbose = 0

        self._servers_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'db', 'dev')
        self._servers_file = "dev_data.json"

        self.client = os.environ.get('THE_CLIENT')
        self.environment = os.environ.get('THE_ENVIRONMENT')
        self.group = os.environ.get('THE_GROUP')
        self.role = os.environ.get('THE_ROLE')
        self.location = os.environ.get('THE_LOCATION')

        if not self.client:
            self.client = 'test_dev'


class TestConfig(Config):
    """Testing Configuration class

    This class inherits the attributes of the Config class.
    """
    def __init__(self):
        self.verbose = 0

        self._servers_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'db', 'test')
        self._servers_file = "test_data.json"

        self.client = os.environ.get('THE_CLIENT')
        self.environment = os.environ.get('THE_ENVIRONMENT')
        self.group = os.environ.get('THE_GROUP')
        self.role = os.environ.get('THE_ROLE')
        self.location = os.environ.get('THE_LOCATION')

        if not self.client:
            self.client = 'test_test'


class ProdConfig(Config):
    """Production Configuration class

    This class inherits the attributes of the Config class.
    """
    def __init__(self):
        self.verbose = 0

        self._servers_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'db', 'prod')
        self._servers_file = "data.json"

        self.client = os.environ.get('THE_CLIENT')
        self.environment = os.environ.get('THE_ENVIRONMENT')
        self.group = os.environ.get('THE_GROUP')
        self.role = os.environ.get('THE_ROLE')
        self.location = os.environ.get('THE_LOCATION')

        if not self.client:
            self.client = 'test_prod'
