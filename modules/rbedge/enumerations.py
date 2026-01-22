from enum import IntEnum, IntFlag


# ref: [UIModalPresentationStyle | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uimodalpresentationstyle)
class UIModalPresentationStyle(IntEnum):
  automatic = -2
  none = -1
  fullScreen = 0
  pageSheet = 1
  formSheet = 2
  currentContext = 3
  custom = 4
  overFullScreen = 5
  overCurrentContext = 6
  popover = 7
  blurOverFullScreen = 8


# ref: [UIRectEdge | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uirectedge?language=objc)
class UIRectEdge(IntFlag):
  none = 0
  top = 1 << 0
  left = 1 << 1
  bottom = 1 << 2
  right = 1 << 3
  all = top | left | bottom | right


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


# ref: [UISceneActivationState | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uiscene/activationstate-swift.enum?language=objc)
class UISceneActivationState(IntEnum):
  # ref: [UISceneDefinitions.rs - source](https://docs.rs/objc2-ui-kit/latest/src/objc2_ui_kit/generated/UISceneDefinitions.rs.html#12)
  unattached = -1
  foregroundActive = 0
  foregroundInactive = 1
  background = 2


# ref: [UITableViewStyle | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uitableviewstyle?language=objc)
class UITableViewStyle(IntEnum):
  # ref: [UITableView.rs - source](https://docs.rs/objc2-ui-kit/latest/src/objc2_ui_kit/generated/UITableView.rs.html#19)
  plain = 0
  grouped = 1
  insetGrouped = 2

