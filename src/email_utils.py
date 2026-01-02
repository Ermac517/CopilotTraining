import re

# NOTE: More precise regex for email validation
email_regex = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def is_valid(address):
    # Fixed: Use match (regex already has ^ and $)
    return bool(email_regex.match(address))

def get_domain(email_str):
    # Fixed: Add error handling if '@' is missing
    if "@" not in email_str:
        return ""
    return email_str[email_str.rfind("@") + 1:]

def local_part(email_str):
    # Fixed: Add error handling for malformed email addresses
    if "@" not in email_str:
        return email_str
    return email_str.split("@")[0]

def masked_email(email_str, show=2):
    """
    Mask an email so only *show* chars of the local part remain visible,
    e.g. jo******@example.com
    """
    if not is_valid(email_str):
        raise ValueError("Invalid email address")
    lp, dom = email_str.split("@")
    # Fixed: Always mask at least one character if local part has length > 0
    # If show >= len(lp), reduce show to len(lp) - 1
    if show >= len(lp):
        show = max(0, len(lp) - 1)
    masked = lp[:show] + "*" * (len(lp) - show)
    return masked + "@" + dom