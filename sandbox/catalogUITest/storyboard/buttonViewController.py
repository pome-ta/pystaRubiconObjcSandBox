import ctypes
from pyrubicon.objc.api import ObjCClass, ObjCInstance, objc_method
from pyrubicon.objc.runtime import send_super

from pyrubicon.objc.types import NSInteger

#ObjCClass.auto_rename = True # xxx: ここ含めて全部呼び出し？

UITableViewCell = ObjCClass('UITableViewCell')


class CustomTableViewCell(UITableViewCell):

  @objc_method
  def initWithStyle_reuseIdentifier_(self, style: NSInteger, reuseIdentifier):

    self_ptr = send_super(__class__,
                          self,
                          'initWithStyle:reuseIdentifier:',
                          style,
                          reuseIdentifier,
                          argtypes=[
                            NSInteger,
                            ctypes.c_void_p,
                          ])

    # todo: `self` に再定義しない
    #self = ObjCInstance(self_ptr)
    return ObjCInstance(self_ptr)


class ButtonSystemAddContact(CustomTableViewCell):
  pass


prototypes = [
  ButtonSystemAddContact,
]

