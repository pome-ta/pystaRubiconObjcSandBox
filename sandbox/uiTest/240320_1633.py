from rubicon.objc import ObjCClass
from rubicon.objc.runtime import libobjc

from pprint import pprint

NSString = ObjCClass('NSString')
'''
print(NSString)
pprint(dir(NSString))
'''

print(libobjc)
pprint(dir(libobjc))
