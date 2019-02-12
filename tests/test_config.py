# -*- coding: utf-8 -*-
"""
Filename: test_config
Created on: 07/02/2019
Project name: dynamic_hosts
Author: Carlos Colon
Description: 
Changes:
    06/02/2019     CECR     Initial version
    12/02/2019     CECR     Added tests for location
"""

from dynamic_hosts import configuration

import os
import json
import unittest


class TestDevelopmentConfig(unittest.TestCase):
    _config = None
    _test_words = ''

    def setUp(self):
        self._config = configuration.DevConfig()
        with open("words.json") as f:
            self._test_words = json.load(f)

    def test_dir_name(self):
        self.assertEqual("dev",
                         os.path.basename(self._config.servers_folder),
                         "Folder name is incorrect")
        self.assertEqual("db",
                         os.path.basename(os.path.dirname(self._config.servers_folder)),
                         "Folder name is incorrect")

    def test_file_name(self):
        self.assertEqual("dev_data.json",
                         self._config.servers_file,
                         "DB file name is incorrect")

    def test_client_prop(self):
        for word in self._test_words:
            self._config.client = word

            self.assertEqual(word, self._config.client, "Client name does not match")

    def test_env_prop(self):
        for word in self._test_words:
            os.environ['THE_ENVIRONMENT'] = word
            self._config = configuration.DevConfig()

            self.assertEqual(word, self._config.environment, "Environment name does not match")

        del os.environ['THE_ENVIRONMENT']

    def test_group_prop(self):
        for word in self._test_words:
            os.environ['THE_GROUP'] = word
            self._config = configuration.DevConfig()

            self.assertEqual(word, self._config.group, "Group name does not match")

        del os.environ['THE_GROUP']

    def test_role_prop(self):
        for word in self._test_words:
            os.environ['THE_ROLE'] = word
            self._config = configuration.DevConfig()

            self.assertEqual(word, self._config.role, "Role name does not match")

        del os.environ['THE_ROLE']

    def test_location_prop(self):
        for word in self._test_words:
            os.environ['THE_LOCATION'] = word
            self._config = configuration.DevConfig()

            self.assertEqual(word, self._config.location, "Location name does not match")

        del os.environ['THE_LOCATION']


class TestTestingConfig(unittest.TestCase):
    _config = None
    _test_words = ''

    def setUp(self):
        self._config = configuration.TestConfig()
        with open("words.json") as f:
            self._test_words = json.load(f)

    def test_dir_name(self):
        self.assertEqual("test",
                         os.path.basename(self._config.servers_folder),
                         "Folder name is incorrect")
        self.assertEqual("db",
                         os.path.basename(os.path.dirname(self._config.servers_folder)),
                         "Folder name is incorrect")

    def test_file_name(self):
        self.assertEqual("test_data.json",
                         self._config.servers_file,
                         "DB file name is incorrect")

    def test_client_prop(self):
        for word in self._test_words:
            self._config.client = word

            self.assertEqual(word, self._config.client, "Client name does not match")

    def test_env_prop(self):
        for word in self._test_words:
            os.environ['THE_ENVIRONMENT'] = word
            self._config = configuration.TestConfig()

            self.assertEqual(word, self._config.environment, "Environment name does not match")

        del os.environ['THE_ENVIRONMENT']

    def test_group_prop(self):
        for word in self._test_words:
            os.environ['THE_GROUP'] = word
            self._config = configuration.TestConfig()

            self.assertEqual(word, self._config.group, "Group name does not match")

        del os.environ['THE_GROUP']

    def test_role_prop(self):
        for word in self._test_words:
            os.environ['THE_ROLE'] = word
            self._config = configuration.TestConfig()

            self.assertEqual(word, self._config.role, "Role name does not match")

        del os.environ['THE_ROLE']

    def test_location_prop(self):
        for word in self._test_words:
            os.environ['THE_LOCATION'] = word
            self._config = configuration.TestConfig()

            self.assertEqual(word, self._config.location, "Location name does not match")

        del os.environ['THE_LOCATION']


class TestProductionConfig(unittest.TestCase):
    _config = None
    _test_words = ''

    def setUp(self):
        self._config = configuration.ProdConfig()
        with open("words.json") as f:
            self._test_words = json.load(f)

    def test_dir_name(self):
        self.assertEqual("prod",
                         os.path.basename(self._config.servers_folder),
                         "Folder name is incorrect")
        self.assertEqual("db",
                         os.path.basename(os.path.dirname(self._config.servers_folder)),
                         "Folder name is incorrect")

    def test_file_name(self):
        self.assertEqual("data.json",
                         self._config.servers_file,
                         "DB file name is incorrect")

    def test_client_prop(self):
        for word in self._test_words:
            self._config.client = word

            self.assertEqual(word, self._config.client, "Client name does not match")

    def test_env_prop(self):
        for word in self._test_words:
            os.environ['THE_ENVIRONMENT'] = word
            self._config = configuration.ProdConfig()

            self.assertEqual(word, self._config.environment, "Environment name does not match")

        del os.environ['THE_ENVIRONMENT']

    def test_group_prop(self):
        for word in self._test_words:
            os.environ['THE_GROUP'] = word
            self._config = configuration.ProdConfig()

            self.assertEqual(word, self._config.group, "Group name does not match")

        del os.environ['THE_GROUP']

    def test_role_prop(self):
        for word in self._test_words:
            os.environ['THE_ROLE'] = word
            self._config = configuration.ProdConfig()

            self.assertEqual(word, self._config.role, "Role name does not match")

        del os.environ['THE_ROLE']

    def test_location_prop(self):
        for word in self._test_words:
            os.environ['THE_LOCATION'] = word
            self._config = configuration.ProdConfig()

            self.assertEqual(word, self._config.location, "Location name does not match")

        del os.environ['THE_LOCATION']


if __name__ == '__main__':
    unittest.main(verbosity=2)
