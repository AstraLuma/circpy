"""
Pathlib, with enhancements
"""
try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib
import os
from datetime import datetime, timezone

PurePath = pathlib.PurePath
PurePosixPath = pathlib.PurePosixPath


class Path(pathlib.Path):
    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        if cls is Path:
            cls = WindowsPath if os.name == 'nt' else PosixPath
        return super().__new__(cls, *args, **kwargs)

    def write_bytes(self, data: bytes, *, mtime=None):
        super().write_bytes(data)
        if mtime is not None:
            atime = self.stat().st_atime
            os.utime(self, (atime, mtime.timestamp()))

    def read_text(self) -> str:
        return self.read_bytes().decode('utf-8')

    def write_text(self, data: str, *, mtime=None):
        self.write_bytes(data.encode('utf-8'), mtime=mtime)

    def mtime(self):
        return datetime.fromtimestamp(
            self.stat().st_mtime,
            timezone.utc
        )

    if not hasattr(pathlib.Path, 'walk'):

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

                paths += [path._make_child_relpath(d)
                          for d in reversed(dirnames)]


class PosixPath(Path, pathlib.PurePosixPath):
    """Path subclass for non-Windows systems.

    On a POSIX system, instantiating a Path should return this object.
    """
    __slots__ = ()


class WindowsPath(Path, pathlib.PureWindowsPath):
    """Path subclass for Windows systems.

    On a Windows system, instantiating a Path should return this object.
    """
    __slots__ = ()

    def is_mount(self):
        raise NotImplementedError(
            "Path.is_mount() is unsupported on this system")
