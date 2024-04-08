from pyrubicon.objc.api import ObjCClass

import pdbr


app = ObjCClass('UIApplication').sharedApplication

pdbr.state(app)
