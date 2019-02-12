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
    _max_tests = 500

    def setUp(self):
        """Setting up DB tests"""
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "words.json")) as f:
            self._test_words = json.load(f)

        test_counter = 0

        """Let's create a test DB"""
        self._config = configuration.TestConfig()
        self._db = ServersDB(self._config)

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

            if len(self._db.get_servers('host', server_data['host'])) == 0:
                new_server = Server(server_data)
                self._db.add_new_server(new_server)

            if test_counter == self._max_tests:
                break

    def tearDown(self):
        """Cleaning up DB Tests"""
        if self._config and os.path.isfile(self._config.get_db_file()):
            os.remove(self._config.get_db_file())
            time.sleep(2.5)  # sleep time in seconds

        self._db = None
        self._config = None

    def test_dev_instance(self):
        """Testing Development instance"""
        self._config = configuration.DevConfig()
        self._db = ServersDB(self._config)

        self.assertIsInstance(self._db, ServersDB)

    def test_test_instance(self):
        """Testing Test instance"""
        self._config = configuration.TestConfig()
        self._db = ServersDB(self._config)

        self.assertIsInstance(self._db, ServersDB)

    def test_prod_instance(self):
        """Testing Production instance"""
        self._config = configuration.ProdConfig()
        self._db = ServersDB(self._config)

        self.assertIsInstance(self._db, ServersDB)

    def test_server_object(self):
        """Testing ServerDB object"""
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
        """Testing Server exceptions"""
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
        """Testing exceptions when adding new server records"""
        self._config = configuration.TestConfig()
        self._db = ServersDB(self._config)

        test_counter = 0

        for word in self._test_words:
            test_counter += 1
            host = "{}{}.{}{}".format(word, word, word, word)

            record = self._db.get_servers('host', host)

            if len(record) == 1:
                with self.assertRaises(Exception) as context:
                    self._db.add_new_server(record[0])

                self.assertTrue('Duplicated data' in str(context.exception))

            if test_counter == self._max_tests:
                break

    def test_add_servers(self):
        """Testing add new server records"""
        self._config = configuration.TestConfig()
        self._db = ServersDB(self._config)

        test_counter = 0

        for word in self._test_words:
            env = choice(['dev', 'itg', 'pro'])
            role = choice(['app', 'db', 'web', 'zoo'])
            server_data = {}
            test_counter += 1
            server_data['host'] = "{}{}.{}{}.net".format(word, word, word, word)
            server_data['environment'] = env
            server_data['role'] = role
            server_data['location'] = "{}.{}-{}.{}".format(word, word, word, word)

            new_server = Server(server_data)

            self._db.add_new_server(new_server)

            inserted = self._db.get_servers('host', server_data['host'])

            self.assertEqual(inserted[0].get_data(), new_server.get_data())

            if test_counter == self._max_tests:
                break

    def test_update_servers(self):
        """Testing update server records"""
        self._config = configuration.TestConfig()
        self._db = ServersDB(self._config)

        test_counter = 0

        for word in self._test_words:
            server_data = {}

            test_counter += 1

            server_data['host'] = "{}{}.{}{}".format(word, word, word, word)

            record = self._db.get_servers('host', server_data['host'])

            if len(record) == 1:
                _data = record[0].get_data()
                _data['location'] = "{}{}-{}{}".format(word, word, word, word)
                new_data = Server(_data)
                self._db.update_server(new_data)

                updated = self._db.get_servers('host', server_data['host'])

                self.assertEqual(new_data.get_data(), updated[0].get_data())

            if test_counter == self._max_tests:
                break

    def test_delete_server(self):
        """Testing delete server records"""
        self._config = configuration.TestConfig()
        self._db = ServersDB(self._config)

        test_counter = 0

        for word in self._test_words:
            test_counter += 1
            host = "{}{}.{}{}".format(word, word, word, word)

            record = self._db.get_servers('host', host)

            if len(record) == 1:
                self._db.delete_server(record[0])

                erased = self._db.get_servers('host', host)

                self.assertEqual(0, len(erased))

            if test_counter == 10:
                break


if __name__ == '__main__':
    unittest.main()
