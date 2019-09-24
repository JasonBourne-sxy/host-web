import requests


def post(header, url):
    """
    post method
    :param header:
    :param url:
    :return:
    """
    return requests.get(url, headers=header, verify=False)
