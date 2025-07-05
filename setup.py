from auth import get_auth_code, get_access_token_with_auth_code
from pathlib import Path

Path('.storage').mkdir(exist_ok=True)
get_auth_code()
auth_code = input('Paste code from URL:\n>> ')
get_access_token_with_auth_code(auth_code)
