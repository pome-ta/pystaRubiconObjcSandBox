'''
  note: sharedApplication` で何が覗けるか調査
'''
from enum import IntEnum

from pyrubicon.objc.api import ObjCClass, ObjCProtocol
from rbedge import pdbr

ObjCClass.auto_rename = True
ObjCProtocol.auto_rename = True


class UISceneActivationState:
  unattached = -1
  foregroundActive = 0
  foregroundInactive = 1
  background = 2


UIApplication = ObjCClass('UIApplication')
UIWindowScene = ObjCClass('UIWindowScene')
UISceneSessionActivationRequest = ObjCClass('UISceneSessionActivationRequest')
UIWindow = ObjCClass('UIWindow')


class NewWindowScene(UIWindowScene):
  pass


sharedApplication = UIApplication.sharedApplication
connectedScenes = sharedApplication.connectedScenes
objectEnumerator = connectedScenes.objectEnumerator()
#sharedApplication.terminateWithSuccess()

while (windowScene := objectEnumerator.nextObject()):
  if windowScene.activationState == UISceneActivationState.foregroundActive:
    break

#[requestSceneSessionActivation:userActivity:options:errorHandler: | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uiapplication/requestscenesessionactivation(_:useractivity:options:errorhandler:)?language=objc)
#[activateSceneSessionForRequest:errorHandler: | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uiapplication/activatescenesessionforrequest:errorhandler:?language=objc)

#newWindowScene = NewWindowScene.new()
#initWithSession_connectionOptions_
#pdbr.state(newWindowScene)
#sharedApplication.activateSceneSessionForRequest_errorHandler_(newWindowScene, None)

pdbr.state(sharedApplication)
#pdbr.state(UIApplication.new())

#pdbr.state(windowScene)

