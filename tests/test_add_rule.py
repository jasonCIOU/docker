import unittest
from tnnginxconfig.nginx import TN, TNginxParamError, RuleExistError

class TestAddRule(unittest.TestCase):

    def setUp(self):
        self.nc = TN()

    def test_add_rule_to_server_block(self):
        self.nc.add_rule("server", "new_server_rule", "some_value")
        server_block = self.nc._find_server_block()
        self.assertIn(("new_server_rule", "some_value"), server_block['value'])

    def test_add_rule_to_location_block(self):
        self.nc.add_rule("location", "new_location_rule", "some_value", "/example")
        location_block = self.nc._find_location_block(self.nc._find_server_block(), "/example")
        self.assertIn(("new_location_rule", "some_value"), location_block['value'])

    def test_add_existing_rule(self):
        self.nc.add_rule("server", "existing_rule", "some_value")
        with self.assertRaises(RuleExistError):
            self.nc.add_rule("server", "existing_rule", "some_value")

    def test_add_invalid_block_type(self):
        with self.assertRaises(TNginxParamError):
            self.nc.add_rule("invalid_block", "some_rule", "some_value")

if __name__ == '__main__':
    unittest.main()
