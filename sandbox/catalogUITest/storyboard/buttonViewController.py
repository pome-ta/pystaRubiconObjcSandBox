import ctypes
from pyrubicon.objc.api import ObjCClass, ObjCInstance, objc_method
from pyrubicon.objc.runtime import send_super, SEL

from pyrubicon.objc.types import NSInteger

#ObjCClass.auto_rename = True # xxx: ここ含めて全部呼び出し？

UITableViewCell = ObjCClass('UITableViewCell')


class ButtonSystemAddContact(UITableViewCell):

  @objc_method
  def initWithStyle_reuseIdentifier_(self, style: ctypes.c_void_p,
                                     reuseIdentifier):

    send_super(__class__,
               self,
               'initWithStyle:reuseIdentifier:', [
                 style,
                 reuseIdentifier,
               ],
               argtypes=[
                 ctypes.c_void_p,
                 str,
               ])

    #return self
    #cell = ObjCInstance(_cell)
    #return ObjCInstance(_cell).ptr
    return self
    #return cell


prototypes = [
  ButtonSystemAddContact,
]

