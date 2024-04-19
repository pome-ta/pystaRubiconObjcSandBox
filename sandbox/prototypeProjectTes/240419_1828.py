import ctypes

from pyrubicon.objc.api import ObjCInstance, ObjCClass, ObjCProtocol, objc_method
from pyrubicon.objc.runtime import SEL, send_super, Foundation, Class

from mainThread import onMainThread
import pdbr

ObjCClass.auto_rename = True


UIScreenEdgePanGestureRecognizer = ObjCClass('UIScreenEdgePanGestureRecognizer')

#UIRectEdge = Foundation.UIRectEdge

#pdbr.state(UIScreenEdgePanGestureRecognizer)
