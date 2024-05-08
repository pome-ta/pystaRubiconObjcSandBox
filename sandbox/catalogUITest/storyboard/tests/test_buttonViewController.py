import sys
import pathlib

parent_level = 3
sys.path.append(str(pathlib.Path(__file__, '../' * parent_level).resolve()))

try:
  from pyrubicon.objc.api import ObjCClass
  from pyrubicon.objc.runtime import send_super

  from rbedge import present_viewController
  from rbedge import pdbr
except Exception as e:
  # xxx: `(ModuleNotFoundError, LookupError)`
  print(f'{e}: error')

# --- test modules
from storyboard.buttonViewController import prototypes

#ObjCClass.auto_rename = True

UITableViewController = ObjCClass('UITableViewController')


class TableViewControllerTest(UITableViewController):
  pass


if __name__ == '__main__':
  vc = TableViewControllerTest.new()
  present_viewController(vc)

