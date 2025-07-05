from pathlib import Path
from config import STORAGE_DIR

class Storage:
  def __init__(self, filename: str):
    storage_dir = Path(STORAGE_DIR)
    if not storage_dir.exists(): storage_dir.mkdir(parents=True, exist_ok=True)
    self.file = storage_dir / filename
    if not self.file.exists(): self.file.write_text('')   # Create file if needed

  def store(self, data: str) -> int:
    return self.file.write_text(data)

  def retrieve(self) -> str:
    return self.file.read_text()
