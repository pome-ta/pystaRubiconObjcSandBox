from enum import IntEnum


# ref: [UIButtonType | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uibuttontype?language=objc)
class UIButtonType(IntEnum):
  # [UIButton.rs - source](https://docs.rs/objc2-ui-kit/latest/src/objc2_ui_kit/generated/UIButton.rs.html#20-39)
  #[doc(alias = "UIButtonTypeCustom")]
  custom = 0
  #[doc(alias = "UIButtonTypeSystem")]
  system = 1
  #[doc(alias = "UIButtonTypeDetailDisclosure")]
  detailDisclosure = 2
  #[doc(alias = "UIButtonTypeInfoLight")]
  infoLight = 3
  #[doc(alias = "UIButtonTypeInfoDark")]
  infoDark = 4
  #[doc(alias = "UIButtonTypeContactAdd")]
  contactAdd = 5
  #[doc(alias = "UIButtonTypePlain")]
  plain = 6
  #[doc(alias = "UIButtonTypeClose")]
  close = 7
  #[doc(alias = "UIButtonTypeRoundedRect")]
  roundedRect = system

