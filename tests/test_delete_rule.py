import unittest
from tnnginxconfig.nginx import TN

class TestDeleteRule(unittest.TestCase):

    def setUp(self):
        self.nc = TN()

    def test_delete_existing_server_rule(self):
        self.nc.add_rule("server", "existing_server_rule", "some_value")
        self.nc.delete_rule("server", "existing_server_rule")
        server_block = self.nc._find_server_block()
        self.assertNotIn(("existing_server_rule", "some_value"), server_block['value'])

    def test_delete_existing_location_rule(self):
        self.nc.add_rule("location", "existing_location_rule", "some_value", "/example")
        self.nc.delete_rule("location", "existing_location_rule", "/example")
        location_block = self.nc._find_location_block(self.nc._find_server_block(), "/example")
        self.assertNotIn(("existing_location_rule", "some_value"), location_block['value'])

    def test_delete_non_existing_rule(self):
        with self.assertRaises(RuleException):
            self.nc.delete_rule("server", "non_existing_rule")

if __name__ == '__main__':
    unittest.main()


"""
import pytest
from tnginx.nginx import TN
from tnnginxconfig.exceptions import *

SAMPLE_CONFIG = """
server {
    listen 80;
    location / {
        proxy_pass http://localhost:3000;
    }
}
"""

@pytest.fixture
def nginx_config():
    nc = TN()
    nc.loads(SAMPLE_CONFIG)
    return nc

def test_delete_rule_from_server_block(nginx_config):
    nginx_config.delete_rule("server", "listen")
    with pytest.raises(RuleEXception):
        assert ("listen", "80") in nginx_config._find_server_block()["value"]

def test_delete_non_existing_rule_from_server_block(nginx_config):
    with pytest.raises(RuleEXception):
        nginx_config.delete_rule("server", "non_exist_directive")

def test_delete_rule_from_location_block(nginx_config):
    nginx_config.delete_rule("/", "proxy_pass")
    location_block = nginx_config._find_location_block(nginx_config._find_server_block(), "/")
    with pytest.raises(RuleEXception):
        assert ("proxy_pass", "http://localhost:3000") in location_block["value"]

def test_delete_non_existing_rule_from_location_block(nginx_config):
    with pytest.raises(RuleEXception):
        nginx_config.delete_rule("/", "non_exist_directive")

"""