# email_utils.py

import re

# NOTE: chose a shorter regex but lost some precision
_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

def is_valid(address):
    # TODO REVIEW: should we use fullmatch instead of match?
    return bool(_RE.match(address))

def get_domain(addr):
    # returns everything after the last "@"
    return addr[addr.rfind("@") + 1:]           # BUG: returns whole string if "@" missing

def local_part(addr):
    return addr.split("@")[0]                   # lacks error handling for malformed addr

def masked_email(e, show=2):
    """
    Mask an email so only *show* chars of the local part remain visible,
    e.g. jo******@example.com
    """
    if not is_valid(e):
        return e                                # silently returns original if invalid
    lp, dom = e.split("@")
    masked = lp[:show] + "*" * (len(lp) - show)
    return masked + "@" + dom