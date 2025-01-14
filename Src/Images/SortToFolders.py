import sys
from pathlib import Path


def SortToFolders(p: Path, minCount: int = 0):
    files = list(p.glob("*"))
    seqs = set()
    for file in files:
        try:
            fileName = file.stem.replace("_", "")
            if (
                fileName[-2:].strip().isnumeric()
                and int(fileName[-2:]) > minCount
                and file.is_file()
            ):
                seq = " ".join(file.stem.split(" " if fileName == file.stem else "_")[:-1])
                if len([x for x in files if seq in str(x)]) > 1:
                    seqs.add(seq)
        except ValueError as e:
            print(file)
            raise e
    for seq in seqs:
        folder = p / seq
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
        for file in p.glob(f"{seq}*.*"):
            file.replace(p / seq / file.name)
    return f"Folders made for {'\n\t'.join(list(seqs))}"


if __name__ == "__main__":
    path = Path(sys.argv[1])
    if path.exists() and path.is_dir():
        SortToFolders(path)
