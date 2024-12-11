from pathlib import Path

from pdf2image import convert_from_path


def DecompilePDF(inputPath: Path):
    pdfList = list(inputPath.glob("**/*.pdf")) if inputPath.is_dir() else [inputPath]
    writtenTo = []
    for pdf in pdfList:
        dst = Path(str(pdf).replace(".pdf", ""))
        if dst.exists():
            dst = dst.parent / (dst.name + " PDF")
            dst.mkdir(exist_ok=True)
        else:
            dst.mkdir()
        _pages = convert_from_path(
            pdf_path=pdf,
            fmt="png",
            output_file=f'{dst.name.replace(" PDF", "")} ',
            output_folder=dst,
        )
        writtenTo.append(f"{dst.parent.name}\\{dst.name}")
    return f"Written PDFs to {'\t\n'.join(writtenTo)}"
