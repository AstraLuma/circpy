from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
import io
from typing import Self

from .. import _pathlib


class CPPath(ABC):
    """
    Base class for Paths pointing into a CircuitPython device.

    Tries to follow the pathlib.Path interface.
    """
    parent: Self
    # FIXME: Implement the rest of the methods

    def __repr__(self):
        return f'<{type(self).__name__} {self.as_uri()!r}>'

    def __truediv__(self, other):
        if isinstance(other, _pathlib.PurePath):
            other = str(other)

        if '/' in other:
            # Break up and recurse
            thisstep, _, nextstep = other.partition('/')
            nextfile = self / thisstep
            return nextfile / nextstep
        elif other == '.':
            return self
        elif other == '..':
            return self.parent
        else:
            for f in self.iterdir():
                if f.name == other:
                    return f
            else:
                return self._synthesize_child(other)

    @abstractmethod
    def _synthesize_child(self, name):
        """
        Create a fake path that doesn't exist
        """

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
    def write_bytes(self, data: bytes, *, mtime=None):
        ...

    def read_text(self) -> str:
        return self.read_bytes().decode('utf-8')

    def write_text(self, data: str, *, mtime=None):
        self.write_bytes(data.encode('utf-8'), mtime=mtime)

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

    def walk(self, top_down=True, on_error=None, follow_symlinks=False):
        """Walk the directory tree from this directory, similar to os.walk()."""
        paths = [self]

        while paths:
            path = paths.pop()
            if isinstance(path, tuple):
                yield path
                continue

            try:
                scandir_it = path.iterdir()
            except OSError as error:
                if on_error is not None:
                    on_error(error)
                continue

            dirnames = []
            filenames = []
            for entry in scandir_it:
                try:
                    is_dir = entry.is_dir()
                except OSError:
                    # carried over from os.path.isdir().
                    is_dir = False

                if is_dir:
                    dirnames.append(entry.name)
                else:
                    filenames.append(entry.name)

            if top_down:
                yield path, dirnames, filenames
            else:
                paths.append((path, dirnames, filenames))

            paths += [path / d for d in reversed(dirnames)]

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
        return _pathlib.PurePosixPath(*bits)

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
