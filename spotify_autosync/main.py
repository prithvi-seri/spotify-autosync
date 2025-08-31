from .playlists import update_playlists

def handler(event, context):
  print('working...')
  update_playlists()
  print('done.')
  return 'Success!'

if __name__ == '__main__':
  handler(0, 0)
