from .playlists import update_playlists, trim_new_playlist

def handler(event, context):
  if event and event.get('task') == 'trim':
    trim_new_playlist()
  else:
    update_playlists()
  return 'Success!'

if __name__ == '__main__':
  handler(None, None)
