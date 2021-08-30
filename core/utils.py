import re

HEADERS_RE = re.compile(r"([^:]+)\s*:\s*(.*)")

def convert_headers_to_dict(header_string):
    return {k.strip():v.strip() for k, v in HEADERS_RE.findall(header_string)}
