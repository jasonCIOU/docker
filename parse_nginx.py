import pynginxconfig

with open('./nginx.conf', 'r') as f:
    config_data = f.read()

# Create the NginxConfig instance with loaded data
config = pynginxconfig.NginxConfig(config_data)

# Define the new proxy rule structure
proxy_rule_content = {
    "name": "server",
    "param": "",
    "value": [
        ("listen", "8082"),
        ("server_name", "proxy.example.com"),
        {
            "name": "location",
            "param": "/",
            "value": [("proxy_pass", "http://localhost:6001")]
        }
    ]
}

# Append the new rule
config.append(proxy_rule_content)

# Combine the original config and the new server block
combined_config = config_data + "\n" + config.gen_config()

# Save the combined configuration
with open('./nginx.conf', 'w') as f:
    f.write(combined_config)

print("Proxy rule added successfully!")

### 讀取
# # 讀取當前目錄的 nginx.conf 檔案
# config = pynginxconfig.load('./nginx.conf')

# # 使用 modify 方法來修改 proxy_pass 的值
# config.modify([('server', 'server_name proxy.example.com'), ('location', '/'), 'proxy_pass'], 'http://localhost:6002')

# # 儲存修改後的配置到檔案中
# config.dump('./nginx.conf')

###讀取2
# # 載入配置文件
# config = pynginxconfig.load('./nginx.conf')

# # 修改指定的配置
# path_to_modify = [('server', 'listen 8082'), ('location', '/'), 'proxy_pass']
# new_value = "http://newlocation:6002"
# config.modify(path_to_modify, new_value)

# # 儲存修改後的配置
# with open('./nginx_modified.conf', 'w') as f:
#     f.write(str(config))