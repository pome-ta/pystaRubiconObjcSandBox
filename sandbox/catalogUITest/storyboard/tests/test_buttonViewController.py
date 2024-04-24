import sys
import pathlib

parent_level = 3
sys.path.append(str(pathlib.Path(__file__, '../' * parent_level).resolve()))

from pyrubicon.objc.api import ObjCClass, objc_method
from storyboard.buttonViewController import prototypes

