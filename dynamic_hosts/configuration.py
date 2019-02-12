# -*- coding: utf-8 -*-
"""
Filename: configuration
Created on: 07/02/2019
Project name: dynamic_hosts
Author: Carlos Colon
Description: 
Changes:
    06/02/2019     CECR     Initial version
    12/02/2019     CECR     Added location
"""

import os


class Config:
    _verbose = 0

    _servers_folder = ''
    _servers_file = ''

    _client = ''
    _environment = ''
    _group = ''
    _role = ''
    _location = ''

    @property
    def servers_folder(self):
        return self._servers_folder

    @property
    def servers_file(self):
        return self._servers_file

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        if value:
            self._verbose = value

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        if value:
            self._client = value

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, value):
        self._environment = value

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    def get_db_file(self):
        return os.path.join(self._servers_folder, self._client, self._servers_file)


class DevConfig(Config):
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
