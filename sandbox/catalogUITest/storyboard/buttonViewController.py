from pyrubicon.objc.api import ObjCClass, objc_method
from pyrubicon.objc.runtime import send_super


ObjCClass.auto_rename = True # xxx: ここ含めて全部呼び出し？

UITableViewCell = ObjCClass('UITableViewCell')



class ButtonSystemAddContact(UITableViewCell):

  @objc_method
  def initWithStyle_reuseIdentifier_(self, style, reuseIdentifier):
    cell = send_super(__class__, self, 'initWithStyle:reuseIdentifier:')
    print(cell)
    return cell


prototypes = [ButtonSystemAddContact,]

