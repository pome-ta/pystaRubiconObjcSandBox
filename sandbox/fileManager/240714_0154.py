from pathlib import Path

from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.runtime import Foundation, Class

'''
def NSSearchPathForDirectoriesInDomains(directory, domainMask):
  pass
'''

NSSearchPathForDirectoriesInDomains = Foundation.NSSearchPathForDirectoriesInDomains
