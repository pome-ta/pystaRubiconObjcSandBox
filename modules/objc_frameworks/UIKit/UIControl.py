from enum import IntEnum


class UIControlEvents(IntEnum):

  #[doc(alias = "UIControlEventTouchDown")]
  TouchDown = 1 << 0
  #[doc(alias = "UIControlEventTouchDownRepeat")]
  TouchDownRepeat = 1 << 1
  #[doc(alias = "UIControlEventTouchDragInside")]
  TouchDragInside = 1 << 2
  #[doc(alias = "UIControlEventTouchDragOutside")]
  TouchDragOutside = 1 << 3
  #[doc(alias = "UIControlEventTouchDragEnter")]
  TouchDragEnter = 1 << 4
  #[doc(alias = "UIControlEventTouchDragExit")]
  TouchDragExit = 1 << 5
  #[doc(alias = "UIControlEventTouchUpInside")]
  TouchUpInside = 1 << 6
  #[doc(alias = "UIControlEventTouchUpOutside")]
  TouchUpOutside = 1 << 7
  #[doc(alias = "UIControlEventTouchCancel")]
  TouchCancel = 1 << 8
  #[doc(alias = "UIControlEventValueChanged")]
  ValueChanged = 1 << 12
  #[doc(alias = "UIControlEventPrimaryActionTriggered")]
  PrimaryActionTriggered = 1 << 13
  #[doc(alias = "UIControlEventMenuActionTriggered")]
  MenuActionTriggered = 1 << 14
  #[doc(alias = "UIControlEventEditingDidBegin")]
  EditingDidBegin = 1 << 16
  #[doc(alias = "UIControlEventEditingChanged")]
  EditingChanged = 1 << 17
  #[doc(alias = "UIControlEventEditingDidEnd")]
  EditingDidEnd = 1 << 18
  #[doc(alias = "UIControlEventEditingDidEndOnExit")]
  EditingDidEndOnExit = 1 << 19
  #[doc(alias = "UIControlEventAllTouchEvents")]
  AllTouchEvents = 0x00000FFF
  #[doc(alias = "UIControlEventAllEditingEvents")]
  AllEditingEvents = 0x000F0000
  #[doc(alias = "UIControlEventApplicationReserved")]
  ApplicationReserved = 0x0F000000
  #[doc(alias = "UIControlEventSystemReserved")]
  SystemReserved = 0xF0000000
  #[doc(alias = "UIControlEventAllEvents")]
  AllEvents = 0xFFFFFFFF

