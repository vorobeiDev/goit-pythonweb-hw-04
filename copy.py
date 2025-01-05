import argparse
import asyncio
import logging

from aiofiles.os import makedirs
from pathlib import Path
from aioshutil import copyfile

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = parser.parse_args()

source = Path(args.source)
output = Path(args.output)

async def grabs_folder(path: Path):
    try:
        for el in path.iterdir():
            if el.is_dir():
                await grabs_folder(el)
            else:
                await copy_file(el)
    except Exception as e:
        logging.error(f"Error while copying {path}: {e}")


async def copy_file(file_path: Path):
    ext_folder = output / file_path.suffix.lstrip('.') or 'no_extension'
    try:
        await makedirs(ext_folder, exist_ok=True)
        await copyfile(file_path, ext_folder / file_path.name)
        logging.info(f"File {file_path.name} copied to {ext_folder}")
    except OSError as e:
        logging.error(f"Error copying file {file_path.name}: {e}")


if __name__ == "__main__":
    message_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=message_format, datefmt="%H:%M:%S")

    asyncio.run(grabs_folder(source))