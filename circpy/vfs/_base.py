from abc import abstractmethod
from datetime import datetime
import io
import pathlib


class CPPath(pathlib.PurePath):
    """
    Base class for Paths pointing into a CircuitPython device
    """
    @abstractmethod
    def exists(self) -> bool:
        ...

    @abstractmethod
    def is_file(self) -> bool:
        ...

    @abstractmethod
    def is_dir(self) -> bool:
        ...

    @abstractmethod
    def read_bytes(self) -> bytes:
        ...

    @abstractmethod
    def read_text(self) -> str:
        ...

    @abstractmethod
    def write_bytes(self, data: bytes):
        ...

    @abstractmethod
    def write_text(self, data: str):
        ...

    @abstractmethod
    def iterdir(self):
        ...

    @abstractmethod
    def mtime(self) -> datetime:
        ...

    @abstractmethod
    def mkdir(self, parents=False, exist_ok=False):
        ...

    @abstractmethod
    def unlink(self, missing_ok=False):
        ...

    @abstractmethod
    def rmdir(self):
        ...

    @abstractmethod
    def rename(self, target):
        ...

    @abstractmethod
    def replace(self, target):
        ...


class Root(CPPath):
    """
    The CircuitPython device itself.
    """

    @abstractmethod
    def open_term(self) -> io.IOBase:
        """
        Open the serial terminal/REPL.
        """
        ...
