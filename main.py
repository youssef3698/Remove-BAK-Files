# Standard Library Imports
from datetime import datetime
from os import getenv, remove
from pathlib import Path

# Third Party Imports
from dotenv import load_dotenv


def format_bytes(size: int) -> str:
    """Format bytes into readable units

    Args:
        size (int): size in bytes

    Returns:
        str: readable format with appropriate units
    """
    # Define the units in ascending order of size
    units: list[str] = ["B", "kB", "MB", "GB", "TB", "PB"]
    # Keep dividing the size by 1024 and move to the next unit
    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"  # Return in petabytes if size is extremely large


def main() -> None:
    # Get folder path
    load_dotenv(".env")
    folder_path: Path = Path(getenv("FOLDER_PATH"))

    # Initialize counters
    total_counter: int = 0
    removed_counter: int = 0
    removed_bytes: int = 0
    remaining_bytes: int = 0

    # Reccursively search for .bak files
    for file in folder_path.rglob("*.bak"):
        total_counter += 1
        file_mtime: datetime = datetime.fromtimestamp(file.stat().st_mtime)
        today: datetime = datetime.now()
        difference_days: int = (today - file_mtime).days

        # If file is older than 30 days delete
        if difference_days > 30:
            removed_bytes += file.stat().st_size
            removed_counter += 1
            remove(file)
            print(f"{file.name} was removed")

        # If not older than 30 days keep
        else:
            remaining_bytes += file.stat().st_size
            print(
                f"{file.name} was not removed because it was created {difference_days} days ago."
            )

    # Print logs
    # TODO: Should implement logger
    print(f"Files scanned: {total_counter}")
    print(
        f"{removed_counter} files were removed with a total of {format_bytes(removed_bytes)}"
    )
    print(
        f"{total_counter - removed_counter} files remain with a total of {format_bytes(remaining_bytes)}"
    )


if __name__ == "__main__":
    main()
