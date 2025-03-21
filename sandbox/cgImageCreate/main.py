import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSizeMake

from rbedge.functions import NSStringFromClass

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
UIColor = ObjCClass('UIColor')

UIGraphicsImageRenderer = ObjCClass('UIGraphicsImageRenderer')
UIImageView = ObjCClass('UIImageView')


class MainViewController(UIViewController):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'\t - {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    #print(f'\t{NSStringFromClass(__class__)}: loadView')
    #pdbr.state()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    #print(f'\t{NSStringFromClass(__class__)}: viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__) if (
      title := self.navigationItem.title) is None else title

    _size = CGSizeMake(64, 64)
    renderer = UIGraphicsImageRenderer.alloc().initWithSize_(_size)
    '''
    def imageRendererContext(_context: ctypes.c_void_p) -> None:
      context = ObjCInstance(_context)
      context.fillRect_(renderer.format.bounds)
    '''

    image = renderer.imageWithActions_(
      Block(lambda context:None, None, ctypes.c_void_p))
    imageView = UIImageView.alloc().initWithImage_(image)
    
    pdbr.state(imageView)
    
    self.view.addSubview_(imageView)

  '''
  @objc_method
  def imageRendererContext(self, _context:ctypes.c_void_p)->None:
    context = ObjCInstance(_context)
    #pdbr.state(context)
  '''

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')


if __name__ == '__main__':
  from rbedge.app import App
  from rbedge.enumerations import UIModalPresentationStyle

  main_vc = MainViewController.new()

  #presentation_style = UIModalPresentationStyle.fullScreen
  presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

