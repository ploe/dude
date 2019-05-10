import unittest
from time import sleep

import docker

from Databank import Databank

class DatabankTestCase(unittest.TestCase):
    def tearDown(self):
        self.container.stop()
        self.client.close()


    def setUp(self):
        self.container = self.docker_run_mysql()
        self.databank = Databank("tests/banks/test_Databank.yml")


    def docker_run_mysql(self):
        self.client = docker.from_env()
        mysql = {
            'auto_remove': True,
            'detach': True,
            'environment': {
                'MYSQL_ROOT_PASSWORD': "+zQx57?4$9",
            },
            'image': 'mysql',
            'ports': {'3306/tcp': '3306'},
        }

        container = self.client.containers.run(**mysql)
        sleep(15)

        return container


    def test_init(self):
        self.assertTrue(self.databank)
        self.assertEqual(self.databank.data['driver'], "MySQL")
        self.assertTrue(self.databank.data['login'])


    def test_connect(self):
        driver = self.databank.connect()
        self.assertTrue(driver)
        
