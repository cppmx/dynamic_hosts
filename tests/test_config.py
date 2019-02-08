# -*- coding: utf-8 -*-
"""
Filename: test_config
Created on: 07/02/2019
Project name: dynamic_hosts
Author: Carlos Colon
Description: 
Changes:
    06/02/2019     CECR     Initial version
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

    def test_folder_name(self):
        self.assertEqual("servers",
                         os.path.basename(self._config.servers_folder),
                         "Folder name is incorrect")

    def test_dir_name(self):
        self.assertEqual("dev",
                         os.path.basename(os.path.dirname(self._config.servers_folder)),
                         "Folder name is incorrect")

    def test_file_name(self):
        self.assertEqual("servers.json",
                         self._config.servers_file,
                         "DB file name is incorrect")

    def test_db_file_no_client(self):
        self.assertEqual("servers.json",
                         os.path.basename(self._config.get_db_file()),
                         "Folder name is incorrect")
        self.assertEqual("servers",
                         os.path.basename(os.path.dirname(self._config.get_db_file())),
                         "Folder name is incorrect")

    def test_db_file_some_client(self):
        self.assertEqual("servers.json",
                         os.path.basename(self._config.get_db_file('test')),
                         "Folder name is incorrect")
        self.assertEqual("some_client",
                         os.path.basename(os.path.dirname(self._config.get_db_file('some_client'))),
                         "Folder name is incorrect")

    def test_client_prop(self):
        for word in self._test_words:
            self._config.client = word

            self.assertEqual(word, self._config.client, "Client name does not match")

    def test_env_prop(self):
        for word in self._test_words:
            self._config.environment = word

            self.assertEqual(word, self._config.environment, "Environment name does not match")

    def test_group_prop(self):
        for word in self._test_words:
            self._config.group = word

            self.assertEqual(word, self._config.group, "Group name does not match")

    def test_role_prop(self):
        for word in self._test_words:
            self._config.role = word

            self.assertEqual(word, self._config.role, "Role name does not match")


class TestTestingConfig(unittest.TestCase):
    _config = None
    _test_words = ''

    def setUp(self):
        self._config = configuration.TestConfig()
        with open("words.json") as f:
            self._test_words = json.load(f)

    def test_folder_name(self):
        self.assertEqual("servers",
                         os.path.basename(self._config.servers_folder),
                         "Folder name is incorrect")

    def test_dir_name(self):
        self.assertEqual("test",
                         os.path.basename(os.path.dirname(self._config.servers_folder)),
                         "Folder name is incorrect")

    def test_file_name(self):
        self.assertEqual("servers.json",
                         self._config.servers_file,
                         "DB file name is incorrect")

    def test_db_file_no_client(self):
        self.assertEqual("servers.json",
                         os.path.basename(self._config.get_db_file()),
                         "Folder name is incorrect")
        self.assertEqual("servers",
                         os.path.basename(os.path.dirname(self._config.get_db_file())),
                         "Folder name is incorrect")

    def test_db_file_some_client(self):
        self.assertEqual("servers.json",
                         os.path.basename(self._config.get_db_file('test')),
                         "Folder name is incorrect")
        self.assertEqual("some_client",
                         os.path.basename(os.path.dirname(self._config.get_db_file('some_client'))),
                         "Folder name is incorrect")

    def test_client_prop(self):
        for word in self._test_words:
            self._config.client = word

            self.assertEqual(word, self._config.client, "Client name does not match")

    def test_env_prop(self):
        for word in self._test_words:
            self._config.environment = word

            self.assertEqual(word, self._config.environment, "Environment name does not match")

    def test_group_prop(self):
        for word in self._test_words:
            self._config.group = word

            self.assertEqual(word, self._config.group, "Group name does not match")

    def test_role_prop(self):
        for word in self._test_words:
            self._config.role = word

            self.assertEqual(word, self._config.role, "Role name does not match")


class TestProductionConfig(unittest.TestCase):
    _config = None
    _test_words = ''

    def setUp(self):
        self._config = configuration.ProdConfig()
        with open("words.json") as f:
            self._test_words = json.load(f)

    def test_folder_name(self):
        self.assertEqual("servers",
                         os.path.basename(self._config.servers_folder),
                         "Folder name is incorrect")

    def test_dir_name(self):
        self.assertEqual("dynamic_hosts",
                         os.path.basename(os.path.dirname(self._config.servers_folder)),
                         "Folder name is incorrect")

    def test_file_name(self):
        self.assertEqual("servers.json",
                         self._config.servers_file,
                         "DB file name is incorrect")

    def test_db_file_no_client(self):
        self.assertEqual("servers.json",
                         os.path.basename(self._config.get_db_file()),
                         "Folder name is incorrect")
        self.assertEqual("servers",
                         os.path.basename(os.path.dirname(self._config.get_db_file())),
                         "Folder name is incorrect")

    def test_db_file_some_client(self):
        self.assertEqual("servers.json",
                         os.path.basename(self._config.get_db_file('test')),
                         "Folder name is incorrect")
        self.assertEqual("some_client",
                         os.path.basename(os.path.dirname(self._config.get_db_file('some_client'))),
                         "Folder name is incorrect")

    def test_client_prop(self):
        for word in self._test_words:
            self._config.client = word

            self.assertEqual(word, self._config.client, "Client name does not match")

    def test_env_prop(self):
        for word in self._test_words:
            self._config.environment = word

            self.assertEqual(word, self._config.environment, "Environment name does not match")

    def test_group_prop(self):
        for word in self._test_words:
            self._config.group = word

            self.assertEqual(word, self._config.group, "Group name does not match")

    def test_role_prop(self):
        for word in self._test_words:
            self._config.role = word

            self.assertEqual(word, self._config.role, "Role name does not match")


if __name__ == '__main__':
    unittest.main()
