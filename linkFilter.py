#!/usr/bin/env python3
# TODO: Implement !=, IN, NOT IN | Multithreading
import sys
from os.path import isfile

__import__("urllib3").disable_warnings()

"""
Simple script to filter urls
"""

FILTERS = ["extension", "domain", "start", "has", "protocol", "status"]

def show_usage():
    print("""./linkFilter.py [url_file.txt] "[expression]" (e.g: ./linkFilter url_file.txt "extension='.js',domain=example.txt,status=200")

[*] Available filters:
    - extension
    - domain
    - start
    - has
    - protocol
    - status
""")

def get_urls(raw_input):
    url = __import__("re").findall("(http|https|ftp|ws):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", raw_input)
    return url

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
    ok_flag = False
    full_url = "".join(url_parts)
    for expression in expressions:
        [key, value] = expression.split("=")
        if key == "extension":
            ok_flag = endpoint.endswith(value)
        elif key == "has":
            ok_flag = value in full_url.lower()
        elif key == "domain":
            ok_flag = value in domain 
        elif key == "status":
            full_url = protocol + "://" + domain + endpoint
            ok_flag = __import__("requests").get(full_url, verify=False).status_code == int(value)
        elif key == "protocol":
            ok_flag = protocol == value 

    return ok_flag
    

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
