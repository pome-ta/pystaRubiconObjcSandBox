from enum import IntEnum, IntFlag


# ref: [UIBarButtonSystemItem | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uibarbuttonsystemitem?language=objc)
class UIBarButtonSystemItem(IntEnum):
  done = 0
  cancel = 1
  edit = 2
  add = 4
  flexibleSpace = 5
  fixedSpace = 6
  compose = 7
  reply = 8
  action = 9
  organize = 10
  bookmarks = 11
  search = 12
  refresh = 13
  stop = 14
  trash = 16
  play = 17
  pause = 18
  rewind = 19
  fastForward = 20
  undo = 21
  redo = 22
  pageCurl = 23  # Deprecated
  close = 24

