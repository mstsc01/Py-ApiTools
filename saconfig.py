
from configparser import ConfigParser
# 保存配置
def save_config(filename, section, settings):
    config = ConfigParser()
    config.add_section(section)
    for key, value in settings.items():
        config.set(section, key, value)
    with open(filename, 'w') as configfile:
        config.write(configfile)

# 读取配置
def read_config(filename, section, key):
    config = ConfigParser()
    config.read(filename)
    return config.get(section, key)

# 保存配置示例
# settings = {
#     'host': '127.0.0.1',
#     'port': '8080'
# }
# save_config('app.ini', 'Server', settings)

# # 读取配置示例
# server_host = read_config('app.ini', 'Server', 'host')
# print(f"Server Host: {server_host}")