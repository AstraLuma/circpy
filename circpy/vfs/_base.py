from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
import io
import pathlib
from typing import Self


class CPPath(ABC):
    """
    Base class for Paths pointing into a CircuitPython device.

    Tries to follow the pathlib.Path interface.
    """
    parent: Self
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
                yield from child.walk()
            else:
                yield child

    def relative_to(self, other):
        """Return the relative path to another path identified by the passed
        arguments.  If the operation is not possible (because this is not
        related to the other path), raise ValueError.
        """
        def parents(dir):
            yield dir
            while dir.parent != dir:
                dir = dir.parent
                yield dir
        for step, path in enumerate(parents(other)):
            if self.is_relative_to(path):
                break
        else:
            raise ValueError(
                f"{str(self)!r} and {str(other)!r} have different anchors")

        bits = []
        for parent in parents(self):
            bits.append(parent.name)
            if parent == path:
                break

        bits = list(reversed(bits[:-1]))
        return pathlib.PurePosixPath(*bits)

    def is_relative_to(self, other):
        """Return True if the path is relative to another path or False.
        """
        def parents(dir):
            yield dir
            while dir.parent != dir:
                dir = dir.parent
                yield dir
        return other in parents(self)


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
