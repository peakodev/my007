from pathlib import Path

current_dir = Path(__file__).resolve().parent
data_dir = current_dir.parent / 'data'
data_dir.mkdir(parents=True, exist_ok=True)


def datadir():
    return data_dir
