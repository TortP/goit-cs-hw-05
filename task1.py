import argparse
import asyncio
import os
from pathlib import Path
import shutil
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def read_folder(source_folder: Path, output_folder: Path):
    """Асинхронно читає файли з вихідної папки і викликає copy_file для кожного з них."""
    tasks = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = Path(root) / file
            tasks.append(copy_file(file_path, output_folder))
    await asyncio.gather(*tasks)


async def copy_file(file_path: Path, output_folder: Path):
    """Асинхронно копіює файл до відповідної підпапки в залежності від розширення."""
    try:
        extension = file_path.suffix.lstrip('.').lower() or "unknown"
        target_folder = output_folder / extension
        target_folder.mkdir(parents=True, exist_ok=True)
        target_file = target_folder / file_path.name

        # Виконуємо копіювання
        await asyncio.to_thread(shutil.copy2, file_path, target_file)
        logging.info(f"Файл {file_path} успішно скопійовано до {target_file}")
    except Exception as e:
        logging.error(f"Помилка під час копіювання файлу {file_path}: {e}")


def main():
    # Налаштування аргументів командного рядка
    parser = argparse.ArgumentParser(
        description="Сортування файлів за розширеннями асинхронно.")
    parser.add_argument("source_folder", type=str,
                        help="Шлях до вихідної папки.")
    parser.add_argument("output_folder", type=str,
                        help="Шлях до папки призначення.")
    args = parser.parse_args()

    source_folder = Path(args.source_folder)
    output_folder = Path(args.output_folder)

    if not source_folder.is_dir():
        logging.error(f"Вказана вихідна папка {
                      source_folder} не існує або не є папкою.")
        return

    output_folder.mkdir(parents=True, exist_ok=True)

    # Запуск основної асинхронної функції
    asyncio.run(read_folder(source_folder, output_folder))


if __name__ == "__main__":
    main()
