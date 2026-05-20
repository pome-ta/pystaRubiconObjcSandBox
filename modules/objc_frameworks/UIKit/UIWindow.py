from .constants import _get_const


class NSNotificationName:
  didBecomeVisibleNotification = _get_const(
    'UIWindowDidBecomeVisibleNotification')
  didBecomeHiddenNotification = _get_const(
    'UIWindowDidBecomeHiddenNotification')
  didBecomeKeyNotification = _get_const('UIWindowDidBecomeKeyNotification')
  didResignKeyNotification = _get_const('UIWindowDidResignKeyNotification')
  keyboardWillShowNotification = _get_const('UIKeyboardWillShowNotification')
  keyboardDidShowNotification = _get_const('UIKeyboardDidShowNotification')
  keyboardWillHideNotification = _get_const('UIKeyboardWillHideNotification')
  keyboardDidHideNotification = _get_const('UIKeyboardDidHideNotification')
  keyboardWillChangeFrameNotification = _get_const(
    'UIKeyboardWillChangeFrameNotification')
  keyboardDidChangeFrameNotification = _get_const(
    'UIKeyboardDidChangeFrameNotification')

