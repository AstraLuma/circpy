from datetime import datetime

from . import _base


class WebPath(_base.CPPath):
    def __init__(self, url, metadata):
        """
        :meta private:
        """

    def exists(self) -> bool:
        ...

    def is_file(self) -> bool:
        ...

    def is_dir(self) -> bool:
        ...

    def read_bytes(self) -> bytes:
        ...

    def read_text(self) -> str:
        ...

    def write_bytes(self, data: bytes):
        ...

    def write_text(self, data: str):
        ...

    def iterdir(self):
        ...

    def mtime(self) -> datetime:
        ...

    def mkdir(self, parents=False, exist_ok=False):
        ...

    def unlink(self, missing_ok=False):
        ...

    def rmdir(self):
        ...

    def rename(self, target):
        ...

    def replace(self, target):
        ...


class WebWorkflow(_base.Root):
    def __init__(self, hostname):
        ...
