'''
  note: sharedApplication` で何が覗けるか調査
'''

from pyrubicon.objc.api import ObjCClass
from rbedge import pdbr

UIApplication = ObjCClass('UIApplication')
#MXMetricManager = ObjCClass('MXMetricManager')

sharedApplication = UIApplication.sharedApplication
#connectedScenes = sharedApplication.connectedScenes
#sharedApplication.terminateWithSuccess()


print(sharedApplication.supportsMultipleScenes)
#pdbr.state(sharedApplication)
#pdbr.state(connectedScenes)
