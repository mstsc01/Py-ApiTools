import json

def all(raw):
    raw = raw.strip()
    # proxy = kwargs.get("proxy", None)
    # real_host = kwargs.get("real_host", None)
    # ssl = kwargs.get("ssl", False)
    # location = kwargs.get("location", True)

    scheme = 'http'
    port = 80
    if any(raws in raw for raws in ["https","sec-"]) :
        scheme = 'https'
        port = 443

    try:
        index = raw.index('\n')
    except ValueError:
        raise Exception("ValueError")
    log = {}
    try:
        method, path, protocol = raw[:index].split(" ")
    except:
        raise Exception("Protocol format error")
    raw = raw[index + 1:]

    try:
        host_start = raw.index("Host: ")
        host_end = raw.index('\n', host_start)

    except ValueError:
        raise ValueError("Host headers not found")
    Cookie=""
    if "Cookie" in raw:
        try:
            Cookie_start = raw.index("Cookie: ")
            Cookie_end = raw.index('\n', Cookie_start)
            Cookie = raw[Cookie_start + len("Cookie: "):Cookie_end]
        except ValueError:
            raise ValueError("Host headers not found")   


    
    real_host=None
    if real_host:
        host = real_host
        if ":" in real_host:
            host, port = real_host.split(":")
    else:
        host = raw[host_start + len("Host: "):host_end]
        if ":" in host:
            host, port = host.split(":")
    raws = raw.splitlines()
    headers = {}

    # index = 0
    # for r in raws:
    #     raws[index] = r.lstrip()
    #     index += 1

    index = 0
    for r in raws:
        if r == "":
            break
        try:
            k, v = r.split(": ")
        except:
            k = r
            v = ""
        headers[k] = v
        index += 1
    headers["Connection"] = "close"
    if len(raws) < index + 1:
        body = ''
    else:
        body = '\n'.join(raws[index + 1:]).lstrip()

   

    return scheme, host, port, path,method,body,headers,Cookie

raw="""
accept:
*/*
accept-encoding:
gzip, deflate, br, zstd
accept-language:
zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
cache-control:
no-cache
connection:
keep-alive
content-length:
44
content-type:
application/x-www-form-urlencoded; text/xml; charset=UTF-8
cookie:
loginUrl=loginSimple; FactoryName=Huawei; FactoryLogoUrl=../../style/default/image/; Package=NO; language=property-zh_CN.js; ARlanguage=property-zh_CN.js
host:
200.3.38.214
origin:
https://200.3.38.214
pragma:
no-cache
referer:
https://200.3.38.214/view/loginSimple.html
sec-ch-ua:
"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"
sec-ch-ua-mobile:
?0
sec-ch-ua-platform:
"Windows"
sec-fetch-dest:
empty
sec-fetch-mode:
cors
sec-fetch-site:
same-origin
user-agent:
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36
"""
# print(all(raw))
# 去除原始字符串的首尾空白字符，包括不可见的 \r
# raw = raw.strip()

# # 按行分割字符串
# lines = raw.split('\n')

# # 创建字典来存储请求头
# headers_str = ""
# headers_dict = {}
# # 由于每两行是一个键值对，步长为2遍历处理
# for i in range(0, len(lines), 2):  # 步长为2，从索引0开始
#     if lines[i].strip():  # 确保键的行不是空的
#         key = lines[i].strip()
#         # 确保当前索引+1（即值的行）存在
#         if i + 1 < len(lines):
#             value = lines[i + 1].strip()
#             print(key,value)
#             headers_str+=key+value
#             headers_dict[key]=value

# # print(headers_dict,headers_str)
# headers_str=headers_str.lower()
# value = headers_dict.get("user-agent:", "Default Value")

# print(value)

