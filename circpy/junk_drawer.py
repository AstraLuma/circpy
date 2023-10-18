
def walking_copy(src, dst):
    """
    Walks the source, copying all files to the dst, updating mtime as it goes.
    """
    for sdir, dirnames, filenames in src.walk():
        try:
            dirnames.remove('.git')  # TODO: Other names to ignore?
        except ValueError:
            pass
        ddir = dst / sdir.relative_to(src)
        print(f"{sdir} -> {ddir}")
        ddir.mkdir(exist_ok=True, parents=True)
        for f in filenames:
            sfile = sdir / f
            dfile = ddir / f
            print(f"{sfile} -> {dfile}")
            dfile.write_bytes(sfile.read_bytes(), mtime=sfile.mtime())
