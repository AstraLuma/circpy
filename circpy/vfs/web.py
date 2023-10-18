from datetime import datetime, timezone
import posixpath
from urllib.parse import urlparse

import httpx

from . import _base
from .. import _pathlib


class WebPath(_base.CPPath):
    _client: httpx.Client
    _metadata: dict | None
    _url: str

    def __init__(self, client, url, metadata):
        """
        :meta private:
        """
        self._client = client
        self._url = url
        self._metadata = metadata

    def __str__(self):
        bits = urlparse(self._url)
        return f"{bits.hostname}:{bits.path.removeprefix('/fs')}"

    def _synthesize_child(self, name):
        if self._url.endswith('/'):
            prefix = self._url
        else:
            prefix = self._url + '/'
        return WebPath(self._client, prefix + name, None)

    @property
    def name(self):
        return posixpath.basename(urlparse(self._url).path.rstrip('/'))

    def as_uri(self):
        return self._url

    def exists(self) -> bool:
        return self._metadata is not None

    def is_file(self) -> bool:
        return self._metadata is not None and not self._metadata['directory']

    def is_dir(self) -> bool:
        return self._metadata is not None and self._metadata['directory']

    def read_bytes(self) -> bytes:
        assert self.is_file()
        resp = self._client.get(self._url)
        resp.raise_for_status()
        return resp.content

    def write_bytes(self, data: bytes, *, mtime=None):
        if mtime:
            modtime_ms = mtime.timestamp() * 1000
        else:
            modtime_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        resp = self._client.put(
            self._url, content=data, headers={'X-Timestamp': str(modtime_ms)},
        )
        resp.raise_for_status()
        self._metadata = {
            'name': self.name,
            'directory': False,
            'modified_ns': modtime_ms * 1_000_000,
            'file_size': len(data),
        }

    def iterdir(self):
        assert self.is_dir()
        resp = self._client.get(
            self._url, headers={'Accept': 'application/json'})
        resp.raise_for_status()
        if self._url.endswith('/'):
            prefix = self._url
        else:
            prefix = self._url + '/'
        for item in resp.json():
            if item['directory']:
                url = prefix + item['name'] + '/'
            else:
                url = prefix + item['name']
            obj = WebPath(self._client, url, item)
            obj.parent = self
            yield obj

    def mtime(self) -> datetime:
        assert self.exists()
        return datetime.fromtimestamp(
            self._metadata['modified_ns'] / 1_000_000_000,
            timezone.utc
        )

    def mkdir(self, parents=False, exist_ok=False):
        modtime_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        # TODO: Do actual URL parsing
        if not self._url.endswith('/'):
            self._url += '/'
        resp = self._client.put(
            self._url, headers={'X-Timestamp': str(modtime_ms)})
        resp.raise_for_status()
        self._metadata = {
            'name': posixpath.basename(urlparse(self._url).path.rstrip('/')),
            'directory': True,
            'modified_ns': modtime_ms * 1_000_000,
            'file_size': 0,
        }

    def unlink(self, missing_ok=False):
        resp = self._client.delete(self._url)
        resp.raise_for_status()
        self._metadata = None

    def rmdir(self):
        self.unlink()

    def rename(self, target):
        dest = urlparse(target._url).path
        self._client.request('MOVE', self._url, headers={
                             'X-Destination': dest})
        target._metadata, self._metadata = self._metadata, None

    def replace(self, target):
        if target.exists():
            target.unlink()
        self.rename(target)


class WebWorkflow(WebPath, _base.Root):
    def __init__(self, hostname, password, *, client=None):
        if client is None:
            self._client = httpx.Client(
                auth=('', password),
                transport=httpx.HTTPTransport(retries=2),
                limits=httpx.Limits(
                    max_keepalive_connections=0, max_connections=1)
            )
        else:
            self._client = client

        if '.' not in hostname:
            hostname = f"{hostname}.local"

        self._url = f'http://{hostname}/fs/'
        self._metadata = {
            'name': '',
            'directory': True,
            'modified_ns': 0,
            'file_size': 0,
        }
        self.parent = self

    @property
    def name(self):
        return ''

    def open_term(self):
        raise NotImplementedError
