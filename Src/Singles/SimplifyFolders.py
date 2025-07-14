import hashlib
import sys
from pathlib import Path


def ComputeHash(path: Path) -> bytes:
    h = hashlib.new("sha256")
    with path.open("rb") as f:
        while chunk := f.read(8196):
            h.update(chunk)
    return h.digest()


def AllEqualFiles(folder: Path) -> bool:
    files = [p for p in folder.iterdir() if p.is_file()]

    if len(files) <= 1:
        return True

    firstHash = ComputeHash(files[0])
    for other in files[1:]:
        if ComputeHash(other) != firstHash:
            return False

    return True


def Simplify(inputPath: Path):
    fileList: list[Path | str] = []
    for dirPath in [x for x in inputPath.glob("*") if x.is_dir()]:  # + [inputPath]:
        if dirPath.stem[0] != "_" and dirPath.exists() and dirPath.is_dir():
            files = list(dirPath.glob("*.*"))
            if files and AllEqualFiles(dirPath):
                file = files[0]
                dst = dirPath.parent / f"{dirPath.name}{file.suffix}"
                if not dst.exists():
                    file.rename(dirPath.parent / f"{dirPath.name}{file.suffix}")
                elif ComputeHash(file) == ComputeHash(dst):
                    file.unlink()
                else:
                    raise FileExistsError(file, dst)
                try:
                    if dst.exists():
                        for f in dirPath.glob("**/*"):
                            f.unlink()
                    dirPath.rmdir()
                    fileList.append(files[0])
                except Exception as e:
                    if "WinError 5" not in str(e):
                        print(e, dirPath)
                    fileList.append(f"FAILED -- {dirPath}")

    return f"Made:\n{'\n'.join([str(x) for x in fileList])}"


if __name__ == "__main__":
    p = Path(sys.argv[1])
    result = Simplify(p)
    print(result)
