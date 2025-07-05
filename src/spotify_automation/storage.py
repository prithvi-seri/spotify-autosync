from pathlib import Path
import json
from config import STORAGE_FILEPATH

STORAGE_FILE = Path(STORAGE_FILEPATH)
if not STORAGE_FILE.exists():
  STORAGE_FILE.write_text('{}')   # Create file if needed

def _load() -> dict:
  return json.loads(STORAGE_FILE.read_text())

def store(key: str, value: any) -> int:
  data = _load()
  data[key] = value
  return STORAGE_FILE.write_text(json.dumps(data, indent=2))

def retrieve(field: str) -> str | dict | list | None:
  return _load().get(field)
