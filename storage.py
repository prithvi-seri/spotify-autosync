from pathlib import Path
from config import STORAGE_DIR

class Storage:
  def __init__(self, filename: str):
    self.file = Path(STORAGE_DIR) / filename
    self.file.write_text('')  # Clear file and create if necessary
    storage_dir = Path(STORAGE_DIR)
    if not storage_dir.exists(): storage_dir.mkdir(exist_ok=True)

def store(self, data: str):
  return self.file.write_text(data)

def retrieve(self) -> str:
  return self.file.read_text()
