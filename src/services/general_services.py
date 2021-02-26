import re


def strip_chars(business_name):
    regex = re.compile("[A-Za-z0-9]")
    return_matched = regex.findall(business_name)
    return ''.join(return_matched).lower()


def business_url_return(business_menu_url, **kwargs):
    bu = business_menu_url
    if bu.find("http://") != 0 and bu.find("https://") != 0:
        bu = "http://" + bu
    return bu
