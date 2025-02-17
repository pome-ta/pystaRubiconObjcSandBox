'''
  note: sharedApplication` で何が覗けるか調査
'''

from pyrubicon.objc.api import ObjCClass
from rbedge import pdbr


class UISceneActivationState:
  unattached = -1
  foregroundActive = 0
  foregroundInactive = 1
  background = 2


UIApplication = ObjCClass('UIApplication')

sharedApplication = UIApplication.sharedApplication
connectedScenes = sharedApplication.connectedScenes
objectEnumerator = connectedScenes.objectEnumerator()

while (windowScene := objectEnumerator.nextObject()):
  if windowScene.activationState == UISceneActivationState.foregroundActive:
    break

