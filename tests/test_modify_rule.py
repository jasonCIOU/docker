import unittest
from tnnginxconfig.nginx import TN, TNginxParamError, RuleExistError

class TestModifyRule(unittest.TestCase):

    def setUp(self):
        self.nc = TN()

    def test_modify_existing_server_rule(self):
        self.nc.add_rule("server", "existing_server_rule", "old_value")
        self.nc.modify_rule("server", "existing_server_rule", "new_value")
        server_block = self.nc._find_server_block()
        self.assertIn(("existing_server_rule", "new_value"), server_block['value'])

    def test_modify_existing_location_rule(self):
        self.nc.add_rule("location", "existing_location_rule", "old_value", "/example")
        self.nc.modify_rule("location", "existing_location_rule", "new_value", "/example")
        location_block = self.nc._find_location_block(self.nc._find_server_block(), "/example")
        self.assertIn(("existing_location_rule", "new_value"), location_block['value'])

    def test_modify_non_existing_rule(self):
        with self.assertRaises(RuleException):
            self.nc.modify_rule("server", "non_existing_rule", "some_value")

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

def test_modify_rule_in_server_block(nginx_config):
    nginx_config.modify_rule("server", "listen", "81")
    assert ("listen", "81") in nginx_config._find_server_block()["value"]

def test_modify_non_existing_rule_in_server_block(nginx_config):
    with pytest.raises(RuleEXception):
        nginx_config.modify_rule("server", "non_exist_directive", "value")

def test_modify_rule_in_location_block(nginx_config):
    nginx_config.modify_rule("/", "proxy_pass", "http://localhost:4000")
    location_block = nginx_config._find_location_block(nginx_config._find_server_block(), "/")
    assert ("proxy_pass", "http://localhost:4000") in location_block["value"]

def test_modify_non_existing_rule_in_location_block(nginx_config):
    with pytest.raises(RuleEXception):
        nginx_config.modify_rule("/", "non_exist_directive", "value")
"""