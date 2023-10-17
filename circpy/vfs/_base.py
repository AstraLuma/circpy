from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
import io
import pathlib


class CPPath(ABC):
    """
    Base class for Paths pointing into a CircuitPython device.

    Tries to follow the pathlib.Path interface.
    """
    # FIXME: Implement the rest of the methods

    @abstractmethod
    def as_uri(self):
        ...

    @abstractproperty
    def name(self):
        ...

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

    def __eq__(self, other):
        return self.as_uri() == other.as_uri()

    def walk(self):
        yield self
        for child in self.iterdir():
            if child.is_dir():
                yield from self.iterdir()
            else:
                yield child


class Root(CPPath, ABC):
    """
    The CircuitPython device itself.
    """

    @abstractmethod
    def open_term(self) -> io.IOBase:
        """
        Open the serial terminal/REPL.
        """
        ...
