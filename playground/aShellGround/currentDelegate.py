_TOP_DIR_NAME = 'pystaRubiconObjcSandBox'
_MODULES_DIR_NAME = 'modules'

# todo: `./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME}` にあるpackage のimport 準備
if __name__ == '__main__' and not __file__[:__file__.rfind('/')].endswith(
    _TOP_DIR_NAME):
  import pathlib
  import sys
  __parents = pathlib.Path(__file__).resolve().parents
  for __dir_path in __parents:
    if __dir_path.name == _TOP_DIR_NAME and (__modules_path := __dir_path /
                                             _MODULES_DIR_NAME).exists():
      sys.path.insert(0, str(__modules_path))
      break
  else:
    import warnings
    with warnings.catch_warnings():
      warnings.simplefilter('always', ImportWarning)
      __warning_message = f'./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME} not found in parent directories'
      warnings.warn(__warning_message, ImportWarning)


from pyrubicon.objc.api import ObjCClass
from rbedge import pdbr

UIApplication = ObjCClass('UIApplication')

sharedApplication = UIApplication.sharedApplication
#pdbr.state(sharedApplication.connectedScenes.allObjects())


#print(sharedApplication.connectedScenes.count)

for scene in sharedApplication.connectedScenes.allObjects():
  #session = scene.session
  #pdbr.state(session.persistentIdentifier)
  #print(session.persistentIdentifier)
  #pdbr.state(scene)
  pdbr.state(scene)
  delegate = scene.delegate
  #delegate.resignFirstResponder()
  #resignFirstResponder
  #pdbr.state(delegate)


'''
for count in range(sharedApplication.connectedScenes.count):
  scene = sharedApplication.connectedScenes.countForObject_(count)
  print(scene)
'''



#pdbr.state(sharedApplication.connectedScenes)

