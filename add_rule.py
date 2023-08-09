from pynginxconfig import NginxConfig

# 創建 PyNginxConfig 的實例
config = NginxConfig()

# 使用 load 方法加載文件
config.loadf('./nginx.conf')

# 在指定的 server 塊的 location / 块中添加一個新的規則
config.append_value(['http', 'server', 'location /'], ('add_header', 'X-Test "Hello"'))

# 儲存修改
config.savef('./nginx_new.conf')



# 使用nginx的命令行工具來檢查配置的語法
# nginx -t -c /path/to/your/nginx.conf