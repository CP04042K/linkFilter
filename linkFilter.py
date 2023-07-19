#!/usr/bin/env python3
# TODO: Implement !=, IN, NOT IN | Multithreading | check in response
import sys
from os.path import isfile
import socket
from re import findall

__import__("urllib3").disable_warnings()

"""
Simple script to filter urls
"""

FILTERS = ["extension", "domain", "start", "has", "protocol", "status", "domainonly", "domainandprotocol", "resolveip", "exceptcontain"]
FILTER_PRITORITIES = {
    "1": ["exceptcontain"],
    "2": ["extension", "domain", "start", "has", "protocol", "status"],
    "3": ["domainonly", "domainandprotocol", "resolveip"]
}
FILTER_PRITORITY_GROUP_QUANTITY = 3

def show_usage():
    print("""./linkFilter.py [url_file.txt] "[expression]" (e.g: ./linkFilter url_file.txt "extension='.js',domain=example.txt,status=200")

[*] Available filters:
    - extension
    - domain
    - start
    - has
    - protocol
    - domainonly
    - domainandprotocol
    - resolveip
    - exceptcontain
""")

def get_urls(raw_input):
    url = findall("(http|https|ftp|ws):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])?", raw_input)
    return url

def sort_filters(filters):
    tmp = []
    for i in range(FILTER_PRITORITY_GROUP_QUANTITY):
        tmp.append([])
        
    for filter in filters:
        [key, _] = filter.split("=")
        if key in FILTER_PRITORITIES["1"]:
            tmp[0].append(filter)
        elif key in FILTER_PRITORITIES["2"]:
            tmp[1].append(filter)
        else:
            tmp[2].append(filter)
    result = []

    for i in range(FILTER_PRITORITY_GROUP_QUANTITY):
        result.extend(tmp[i])
    return result

def parse_expression(raw_expression):
    expression = raw_expression.replace("[", "").replace("]", "").split(",")
    final_expression = []
    for filter_str in expression:
        filter_str = filter_str.strip(" ")
        [key, _] = filter_str.split("=")
        if key in FILTERS:
            final_expression.append(filter_str)
    return final_expression

def check_for_expression(url_parts, expressions):
    [protocol, domain, endpoint] = url_parts
    
    expressions = sort_filters(expressions)
    full_url = "".join(url_parts)
    for expression in expressions:
        [key, value] = expression.split("=")
        if key == "extension" and not endpoint.endswith(value):
            return False
        elif key == "has" and not value in full_url.lower():
            return False 
        elif key == "domain" and not value in domain:
            return False 
        elif key == "protocol" and not protocol == value:
            return False
        elif key == "domainonly":
            return print(domain)
        elif key == "domainandprotocol":
            return print(protocol + "://" + domain + "/")   
        elif key == "exceptcontain" and value in full_url:
            return False  
        elif key == "resolveip":                
            try:
                ip = socket.gethostbyname(domain)
                if value == "onlyip":
                    print(ip)
                else:
                    print(f"{domain} => {ip}")
            except Exception:
                print(f"Couldn't resolve {domain}")
            finally:
                return False
    return True
    

def main(args):
    try:
        [_, fname, expression] = sys.argv
    except Exception:
        show_usage()
        exit(1)        
    
    if not isfile(fname):
        print("[!] File not found.")
        exit(1)

    expressions = parse_expression(expression)

    file_content = open(fname, "r").read()
    urls = get_urls(file_content)
    for url_parts in urls:
        if check_for_expression(url_parts, expressions):
            full_url = url_parts[0] + "://" + url_parts[1] + url_parts[2]
            print(full_url)
    
        
if __name__ == "__main__":
    main(sys.argv)
