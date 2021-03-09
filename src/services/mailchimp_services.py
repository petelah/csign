import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError


def check_api_valid(api_key):
    if '-' not in api_key:
        return False
    server = api_key.split('-')
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": api_key, "server": server[1]
    })
    try:
        response = client.ping.get()
        if response['health_status'] == "Everything's Chimpy!":
            return True
    except ApiClientError:
        return False