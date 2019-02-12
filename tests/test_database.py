# -*- coding: utf-8 -*-
"""
Filename: test_database
Created on: 08/02/2019
Project name: dynamic_hosts
Author: Carlos Colon
Description: 
Changes:
    06/02/2019     CECR     Initial version
"""

from dynamic_hosts import configuration
from dynamic_hosts.database import Server
from dynamic_hosts.database import ServersDB
from random import choice

import os
import time
import json
import unittest


class TestDatabase(unittest.TestCase):
    _db = None
    _config = None
    _test_words = ''
    _max_tests = 100

    def setUp(self):
        with open("words.json") as f:
            self._test_words = json.load(f)

    def test_dev_instance(self):
        self._config = configuration.DevConfig()
        self._db = ServersDB(self._config)

        self.assertIsInstance(self._db, ServersDB)

    def test_test_instance(self):
        self._config = configuration.TestConfig()
        self._db = ServersDB(self._config)

        self.assertIsInstance(self._db, ServersDB)

    def test_prod_instance(self):
        self._config = configuration.ProdConfig()
        self._db = ServersDB(self._config)

        self.assertIsInstance(self._db, ServersDB)

    def test_server_object(self):
        test_counter = 0

        for word in self._test_words:
            env = choice(['dev', 'itg', 'pro'])
            role = choice(['app', 'db', 'web', 'zoo'])
            server_data = {}
            test_counter += 1
            server_data['host'] = "{}{}.{}{}".format(word, word, word, word)
            server_data['environment'] = env
            server_data['role'] = role
            server_data['location'] = "{}.{}-{}.{}".format(word, word, word, word)

            new_server = Server(server_data)

            self.assertIsInstance(new_server, Server)
            self.assertEqual(new_server.get_data(), server_data)

            if test_counter == self._max_tests:
                break

    def test_server_exceptions(self):
        test_counter = 0

        for word in self._test_words:
            env = choice(['dev', 'itg', 'pro'])
            server_data = {}
            test_counter += 1
            server_data['host'] = "{}{}.{}{}".format(word, word, word, word)
            server_data['environment'] = env
            server_data['location'] = "{}.{}-{}.{}".format(word, word, word, word)

            with self.assertRaises(Exception) as context:
                Server(server_data)

            self.assertTrue('Invalid data' in str(context.exception))

            if test_counter == self._max_tests:
                break

    def test_add_servers_exceptions(self):
        self._config = configuration.TestConfig()
        self._db = ServersDB(self._config)

        test_counter = 0

        if os.path.isfile(self._config.get_db_file()):
            os.remove(self._config.get_db_file())
            time.sleep(2.5)  # sleep time in seconds

        for word in self._test_words:
            env = choice(['dev', 'itg', 'pro'])
            role = choice(['app', 'db', 'web', 'zoo'])
            server_data = {}
            test_counter += 1
            server_data['host'] = "{}{}.{}{}".format(word, word, word, word)
            server_data['environment'] = env
            server_data['role'] = role
            server_data['location'] = "{}.{}-{}.{}".format(word, word, word, word)

            new_server = Server(server_data)

            self._db.add_new_server(new_server)

            with self.assertRaises(Exception) as context:
                self._db.add_new_server(new_server)

            self.assertTrue('Duplicated data' in str(context.exception))

            if test_counter == self._max_tests:
                break

        if os.path.isfile(self._config.get_db_file()):
            os.remove(self._config.get_db_file())
            time.sleep(2.5)  # sleep time in seconds

    def test_add_servers(self):
        self._config = configuration.TestConfig()
        self._db = ServersDB(self._config)

        test_counter = 0

        if os.path.isfile(self._config.get_db_file()):
            os.remove(self._config.get_db_file())
            time.sleep(2.5)  # sleep time in seconds

        for word in self._test_words:
            env = choice(['dev', 'itg', 'pro'])
            role = choice(['app', 'db', 'web', 'zoo'])
            server_data = {}
            test_counter += 1
            server_data['host'] = "{}{}.{}{}".format(word, word, word, word)
            server_data['environment'] = env
            server_data['role'] = role
            server_data['location'] = "{}.{}-{}.{}".format(word, word, word, word)

            new_server = Server(server_data)

            self._db.add_new_server(new_server)
            inserted = self._db.get_servers('host', server_data['host'])

            self.assertEqual(inserted[0].get_data(), new_server.get_data())

            if test_counter == self._max_tests:
                break

        if os.path.isfile(self._config.get_db_file()):
            os.remove(self._config.get_db_file())
            time.sleep(2.5)  # sleep time in seconds

    def test_update_servers(self):
        self._config = configuration.TestConfig()
        self._db = ServersDB(self._config)

        test_counter = 0

        if os.path.isfile(self._config.get_db_file()):
            os.remove(self._config.get_db_file())
            time.sleep(2.5)  # sleep time in seconds

        for word in self._test_words:
            env = choice(['dev', 'itg', 'pro'])
            role = choice(['app', 'db', 'web', 'zoo'])
            server_data = {}
            update_data = {}

            test_counter += 1

            server_data['host'] = "{}{}.{}{}".format(word, word, word, word)
            server_data['environment'] = env
            server_data['role'] = role
            server_data['location'] = "{}.{}-{}.{}".format(word, word, word, word)

            new_server = Server(server_data)
            self._db.add_new_server(new_server)
            inserted = self._db.get_servers('host', server_data['host'])

            self.assertEqual(inserted[0].get_data(), new_server.get_data())

            update_data['host'] = server_data['host']
            server_data['environment'] = env
            server_data['role'] = role
            update_data['location'] = "{}{}-{}{}".format(word, word, word, word)

            updated_server = Server(server_data)
            self._db.update_server(updated_server)
            updated = self._db.get_servers('host', server_data['host'])

            self.assertEqual(updated_server.get_data(), updated[0].get_data())

            if test_counter == self._max_tests:
                break

        if os.path.isfile(self._config.get_db_file()):
            os.remove(self._config.get_db_file())
            time.sleep(2.5)  # sleep time in seconds

    def test_delete_server(self):
        self._config = configuration.TestConfig()
        self._db = ServersDB(self._config)

        test_counter = 0

        if os.path.isfile(self._config.get_db_file()):
            os.remove(self._config.get_db_file())
            time.sleep(2.5)  # sleep time in seconds

        for word in self._test_words:
            env = choice(['dev', 'itg', 'pro'])
            role = choice(['app', 'db', 'web', 'zoo'])
            server_data = {}
            test_counter += 1
            server_data['host'] = "{}{}.{}{}".format(word, word, word, word)
            server_data['environment'] = env
            server_data['role'] = role
            server_data['location'] = "{}.{}-{}.{}".format(word, word, word, word)

            new_server = Server(server_data)

            self._db.add_new_server(new_server)
            inserted = self._db.get_servers('host', server_data['host'])

            self.assertEqual(inserted[0].get_data(), new_server.get_data())

            self._db.delete_server(inserted[0])
            erased = self._db.get_servers('host', server_data['host'])

            self.assertEqual([], erased)

            if test_counter == 10:
                break

        if os.path.isfile(self._config.get_db_file()):
            os.remove(self._config.get_db_file())
            time.sleep(2.5)  # sleep time in seconds


if __name__ == '__main__':
    unittest.main(verbosity=2)
