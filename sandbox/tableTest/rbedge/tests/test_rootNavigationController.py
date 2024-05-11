import sys
import pathlib

parent_level = 3
sys.path.append(str(pathlib.Path(__file__, '../' * parent_level).resolve()))

from rbedge.rootNavigationController import RootNavigationController

if __name__ == "__main__":
  nv = RootNavigationController.new()

