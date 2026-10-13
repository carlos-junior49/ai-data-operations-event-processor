from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = PROJECT_ROOT / "src"
OUTPUT_FILE = PROJECT_ROOT / "build" / "lambda.zip"


def packege_lambda() -> None:
    if not SOURCE_DIR.is_dir():
        raise FileNotFoundError(f"O diretorio {SOURCE_DIR} nao existe")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(OUTPUT_FILE, "w", ZIP_DEFLATED) as arquive:
        for file in SOURCE_DIR.rglob("*"):
            if not file.is_file():
                continue

            if "__pycache__" in file.parts or file.suffix == ".pyc":
                continue

            if "__pycache__" in file.parts or file.suffix == ".pyo":
                continue

            arquive.write(file, file.relative_to(SOURCE_DIR.parent))

    print(f"Pacote criado: {OUTPUT_FILE}")


if __name__ == "__main__":
    packege_lambda()