import shutil
from pathlib import Path


def Flatten(p: Path, rename: bool = False, delete: bool = False, globPattern="**/*.*"):
    fileCount, folderCount = 0, 0
    for file in p.glob(globPattern):
        if file.parent != p:
            dst = p / f"{file.parent.stem if rename else ''} {file.name}"
            if delete:
                file.rename(dst)
                fileCount += 1
            else:
                fileCount += 1
                shutil.copyfile(str(file), str(dst))
    if delete:
        for file in p.glob("**/*/"):
            folderCount += 1
            file.rmdir()
    return f"{fileCount} Files moved to {p.name}" + (
        f"\n{folderCount} Folders Removed" if delete else ""
    )
