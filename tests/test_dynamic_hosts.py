# -*- coding: utf-8 -*-
"""
Filename: test_dynamic_hosts
Created on: 12/02/2019
Project name: dynamic_hosts
Author: Carlos Colon
Description: 
Changes:
    06/02/2019     CECR     Initial version
"""

from dynamic_hosts import configuration
from dynamic_hosts.database import Server
from dynamic_hosts.database import ServersDB
from dynamic_hosts.dynamic_hosts import DynamicHosts
from random import choice

import os
import json
import time
import unittest


class TestDynamicHosts(unittest.TestCase):
    _db = None
    _config = None
    _test_words = ''
    _max_tests = 500

    def setUp(self):
        """Setting up Dynamic Hosts Test"""
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "words.json")) as f:
            self._test_words = json.load(f)

        self._config = configuration.DevConfig()
        self._db = ServersDB(self._config)

        test_counter = 0

        """Let's create a test DB"""
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
        """Tear down Dynamic Host Test"""
        if os.path.isfile(self._config.get_db_file()):
            os.remove(self._config.get_db_file())
            time.sleep(2.5)  # sleep time in seconds

        self._config = None

    def test_dynamic_hosts_f1(self):
        """Testing only hosts that belong to the DEV environment"""
        os.environ["THE_ENVIRONMENT"] = "dev"
        self._config = configuration.DevConfig()
        dh = DynamicHosts(self._config)
        hosts_list = dh.get_list()

        self.assertEqual("dev", dh.get_environment)

        for host in hosts_list['all']['hosts']:
            find_host = self._db.get_servers('host', host)
            self.assertEqual(1, len(find_host))
            self.assertEqual("dev", find_host[0].get_data()["environment"])

    def test_dynamic_hosts_f2(self):
        """Testing only hosts that belong to the ITG environment"""
        os.environ["THE_ENVIRONMENT"] = "itg"
        self._config = configuration.DevConfig()
        dh = DynamicHosts(self._config)
        hosts_list = dh.get_list()

        self.assertEqual("itg", dh.get_environment)

        for host in hosts_list['all']['hosts']:
            find_host = self._db.get_servers('host', host)
            self.assertEqual(1, len(find_host))
            self.assertEqual("itg", find_host[0].get_data()["environment"])

    def test_dynamic_hosts_f3(self):
        """Testing only hosts that belong to the PRO environment"""
        os.environ["THE_ENVIRONMENT"] = "pro"
        self._config = configuration.DevConfig()
        dh = DynamicHosts(self._config)
        hosts_list = dh.get_list()

        self.assertEqual("pro", dh.get_environment)

        for host in hosts_list['all']['hosts']:
            find_host = self._db.get_servers('host', host)
            self.assertEqual(1, len(find_host))
            self.assertEqual("pro", find_host[0].get_data()["environment"])

    def test_dynamic_hosts_f4(self):
        """Testing only hosts that belong to the APP role"""
        os.environ["THE_ROLE"] = "app"
        self._config = configuration.DevConfig()
        dh = DynamicHosts(self._config)
        hosts_list = dh.get_list()

        self.assertEqual("app", dh.get_role)

        for host in hosts_list['all']['hosts']:
            find_host = self._db.get_servers('host', host)
            self.assertEqual(1, len(find_host))
            self.assertEqual("app", find_host[0].get_data()["role"])

    def test_dynamic_hosts_f5(self):
        """Testing only hosts that belong to the DB role"""
        os.environ["THE_ROLE"] = "db"
        self._config = configuration.DevConfig()
        dh = DynamicHosts(self._config)
        hosts_list = dh.get_list()

        self.assertEqual("db", dh.get_role)

        for host in hosts_list['all']['hosts']:
            find_host = self._db.get_servers('host', host)
            self.assertEqual(1, len(find_host))
            self.assertEqual("db", find_host[0].get_data()["role"])

    def test_dynamic_hosts_f6(self):
        """Testing only hosts that belong to the WEB role"""
        os.environ["THE_ROLE"] = "web"
        self._config = configuration.DevConfig()
        dh = DynamicHosts(self._config)
        hosts_list = dh.get_list()

        self.assertEqual("web", dh.get_role)

        for host in hosts_list['all']['hosts']:
            find_host = self._db.get_servers('host', host)
            self.assertEqual(1, len(find_host))
            self.assertEqual("web", find_host[0].get_data()["role"])

    def test_dynamic_hosts_f7(self):
        """Testing only hosts that belong to the ZOO role"""
        os.environ["THE_ROLE"] = "zoo"
        self._config = configuration.DevConfig()
        dh = DynamicHosts(self._config)
        hosts_list = dh.get_list()

        self.assertEqual("zoo", dh.get_role)

        for host in hosts_list['all']['hosts']:
            find_host = self._db.get_servers('host', host)
            self.assertEqual(1, len(find_host))
            self.assertEqual("zoo", find_host[0].get_data()["role"])

    def test_dynamic_hosts_f1_f4(self):
        """Testing only hosts that belong to the dev environment and APP role"""
        os.environ["THE_ENVIRONMENT"] = "dev"
        os.environ["THE_ROLE"] = "app"
        self._config = configuration.DevConfig()
        dh = DynamicHosts(self._config)
        hosts_list = dh.get_list()

        self.assertEqual("dev", dh.get_environment)
        self.assertEqual("app", dh.get_role)

        for host in hosts_list['all']['hosts']:
            find_host = self._db.get_servers('host', host)
            self.assertEqual(1, len(find_host))
            self.assertEqual("dev", find_host[0].get_data()["environment"])
            self.assertEqual("app", find_host[0].get_data()["role"])

    def test_dynamic_hosts_f2_f5(self):
        """Testing only hosts that belong to the ITG environment and DB role"""
        os.environ["THE_ENVIRONMENT"] = "itg"
        os.environ["THE_ROLE"] = "db"
        self._config = configuration.DevConfig()
        dh = DynamicHosts(self._config)
        hosts_list = dh.get_list()

        self.assertEqual("itg", dh.get_environment)
        self.assertEqual("db", dh.get_role)

        for host in hosts_list['all']['hosts']:
            find_host = self._db.get_servers('host', host)
            self.assertEqual(1, len(find_host))
            self.assertEqual("itg", find_host[0].get_data()["environment"])
            self.assertEqual("db", find_host[0].get_data()["role"])

    def test_dynamic_hosts_f3_f6(self):
        """Testing only hosts that belong to the PRO environment and WEB role"""
        os.environ["THE_ENVIRONMENT"] = "pro"
        os.environ["THE_ROLE"] = "web"
        self._config = configuration.DevConfig()
        dh = DynamicHosts(self._config)
        hosts_list = dh.get_list()

        self.assertEqual("pro", dh.get_environment)
        self.assertEqual("web", dh.get_role)

        for host in hosts_list['all']['hosts']:
            find_host = self._db.get_servers('host', host)
            self.assertEqual(1, len(find_host))
            self.assertEqual("pro", find_host[0].get_data()["environment"])
            self.assertEqual("web", find_host[0].get_data()["role"])


if __name__ == '__main__':
    unittest.main()
