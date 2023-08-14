import pytest
from tnginx.nginx import TN
from tnnginxconfig.exceptions import *

# 為了簡單起見，我會使用一個簡單的nginx配置作為測試基礎。你可以根據需要擴展它。
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

def test_add_rule_to_server_block(nginx_config):
    nginx_config.add_rule("server", "access_log", "/path/to/access.log")
    assert ("access_log", "/path/to/access.log") in nginx_config._find_server_block()["value"]

def test_add_existing_rule_to_server_block(nginx_config):
    with pytest.raises(RuleExistError):
        nginx_config.add_rule("server", "listen", "80")

def test_add_rule_to_existing_location_block(nginx_config):
    nginx_config.add_rule("/","proxy_set_header", "X-Real-IP $remote_addr")
    location_block = nginx_config._find_location_block(nginx_config._find_server_block(), "/")
    assert ("proxy_set_header", "X-Real-IP $remote_addr") in location_block["value"]

def test_add_rule_to_new_location_block(nginx_config):
    nginx_config.add_rule("/app/","proxy_pass", "http://localhost:5000")
    location_block = nginx_config._find_location_block(nginx_config._find_server_block(), "/app/")
    assert location_block is not None
    assert ("proxy_pass", "http://localhost:5000") in location_block["value"]

def test_add_existing_rule_to_location_block(nginx_config):
    with pytest.raises(RuleExistError):
        nginx_config.add_rule("/", "proxy_pass", "http://localhost:3000")
