from auth import *

get_auth_code()
auth_code = input('Paste code from URL:\n>> ')
with open('.authorization_code', 'w') as code_file:
  code_file.write(auth_code)
get_access_token_with_auth_code(auth_code)
