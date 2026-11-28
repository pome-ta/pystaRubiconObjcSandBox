from enum import IntEnum


# ref: [UITableViewStyle | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uitableviewstyle?language=objc)
class UITableViewStyle(IntEnum):
  #[UITableView.rs - source](https://docs.rs/objc2-ui-kit/latest/src/objc2_ui_kit/generated/UITableView.rs.html#20-27)
  #[doc(alias = "UITableViewStylePlain")]
  plain = 0
  #[doc(alias = "UITableViewStyleGrouped")]
  grouped = 1
  #[doc(alias = "UITableViewStyleInsetGrouped")]
  insetGrouped = 2

