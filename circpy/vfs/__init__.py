from urllib.parse import urlparse

from . import ble, usb, web


def from_url(url):
    urlbits = urlparse(url)
    # FIXME: Actually parse and select
    return web.WebWorkflow(urlbits.hostname, urlbits.password)
