from pynginxconfig import NginxConfig
from tnnginxconfig.exceptions import *

class TN(NginxConfig):

    def _find_server_block(self):
        """返回名為'server'的數據區塊,如果找不到,則返回None。"""
        for data_block in self.data:
            if isinstance(data_block, dict) and data_block.get('name') == 'server':
                return data_block
        return None

    def _find_location_block(self, server_block, block_param):
        """在指定的server區塊中找到指定的location區塊,如果不存在,返回None。"""
        for location_block in server_block.get('value', []):
            if isinstance(location_block, dict) and location_block.get('param') == block_param:
                return location_block
        return None

    def _add_or_update_rule(self, block, rule_name, rule_value):
        """在指定的區塊中加入或更新一條指令。如果該指令已存在且與提供的值相同,則引發ValueError。"""
        for rule in block.get('value', []):
            if rule[0] == rule_name:
                if rule[1] == rule_value:
                    raise ValueError(f"Directive {rule_name} {rule_value} already exists.")
                else:
                    rule[1] = rule_value
                    return
        block['value'].append((rule_name, rule_value))

    def add_rule_to_block(self, block_param, rule_name, rule_value):
        try:
            server_block = self._find_server_block()
            if not server_block:
                raise TNginxParamError("Server block not found. Couldn't add the new block.")

            if block_param == 'server':
                self._add_or_update_rule(server_block, rule_name, rule_value)
            else:
                location_block = self._find_location_block(server_block, block_param)
                if location_block:
                    self._add_or_update_rule(location_block, rule_name, rule_value)
                elif block_param.startswith("/"):  # 確保只有location區塊是這樣添加的
                    new_block = {
                        'name': 'location',
                        'param': block_param,
                        'value': [(rule_name, rule_value)]
                    }
                    server_block['value'].append(new_block)
                else:
                    raise TNginxParamError(f"Unknown block parameter: {block_param}")

        except ValueError as e:  # 捕捉內部方法可能引發的ValueError
            raise RuleExistError(str(e)) from e

    def modify_rule(self, block_param, rule_name, new_rule_value):
        server_block = self._find_server_block()
        if not server_block:
            raise TNginxParamError("Server block not found. Couldn't modify the rule.")

        # Function to modify rule in the block
        def modify_in_block(block):
            for rule in block.get('value', []):
                if rule[0] == rule_name:
                    rule[1] = new_rule_value
                    return True
            return False

        if block_param == 'server':
            if not modify_in_block(server_block):
                raise RuleEXception(f"Directive {rule_name} not found in server block.")
        else:
            location_block = self._find_location_block(server_block, block_param)
            if location_block:
                if not modify_in_block(location_block):
                    raise RuleEXception(f"Directive {rule_name} not found in {block_param}.")
            else:
                raise TNginxParamError(f"Location block parameter: {block_param} not found.")

    def delete_rule(self, block_param, rule_name):
        server_block = self._find_server_block()
        if not server_block:
            raise TNginxParamError("Server block not found. Couldn't delete the rule.")

        # Function to delete rule in the block
        def delete_from_block(block):
            for index, rule in enumerate(block.get('value', [])):
                if rule[0] == rule_name:
                    del block['value'][index]
                    return True
            return False

        if block_param == 'server':
            if not delete_from_block(server_block):
                raise RuleEXception(f"Directive {rule_name} not found in server block.")
        else:
            location_block = self._find_location_block(server_block, block_param)
            if location_block:
                if not delete_from_block(location_block):
                    raise RuleEXception(f"Directive {rule_name} not found in {block_param}.")
            else:
                raise TNginxParamError(f"Location block parameter: {block_param} not found.")


if __name__ == '__main__':
    nc = TN()
    nc.loadf('./nginx.conf')
    nc.add_rule_to_block("/nab/", "proxy_cache", "http://your_url_here")
    nc.add_rule_to_block("server", "access_log", "/new/path/to/access.log")
    nc.savef('./nginx_modified.conf')
