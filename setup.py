from auth import get_auth_code, get_access_token_with_auth_code
from storage import initalize_storage

get_auth_code()
auth_code = input('Paste code from URL:\n>> ')
get_access_token_with_auth_code(auth_code)
