from pyrubicon.objc.api import ObjCClass
from rbedge import pdbr

UIButtonConfiguration = ObjCClass('UIButtonConfiguration')

config = UIButtonConfiguration.plainButtonConfiguration()
config.title = 'hoge'
pdbr.state(config)
