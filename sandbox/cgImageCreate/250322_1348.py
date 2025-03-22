import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super, load_library
from pyrubicon.objc.types import CGSizeMake

from rbedge.functions import NSStringFromClass

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
UIColor = ObjCClass('UIColor')

UIGraphicsImageRenderer = ObjCClass('UIGraphicsImageRenderer')
UIImageView = ObjCClass('UIImageView')
CIImage = ObjCClass('CIImage')

CoreGraphics = load_library('CoreGraphics')


# ref: [CGImageGetDataProvider | Apple Developer Documentation](https://developer.apple.com/documentation/coregraphics/cgimage/dataprovider?language=objc)
def CGImageGetDataProvider(image: ctypes.c_void_p) -> ObjCInstance:
  _function = CoreGraphics.CGImageGetDataProvider
  _function.restype = ctypes.c_void_p
  _function.argtypes = [ctypes.c_void_p]
  return ObjCInstance(_function(image))


# ref: [CGDataProviderCopyData | Apple Developer Documentation](https://developer.apple.com/documentation/coregraphics/cgdataprovider/data?language=objc)
def CGDataProviderCopyData(provider: ObjCInstance) -> ObjCInstance:
  _function = CoreGraphics.CGDataProviderCopyData
  _function.restype = ctypes.c_void_p
  _function.argtypes = [ctypes.c_void_p]
  return ObjCInstance(_function(provider))


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

    def imageRendererContext(_context: ctypes.c_void_p) -> None:
      context = ObjCInstance(_context)
      #pdbr.state(context)
      context.fillRect_(renderer.format.bounds)

    image = renderer.imageWithActions_(
      Block(imageRendererContext, None, ctypes.c_void_p))
    #image = renderer.imageWithActions_(Block(lambda context:None, None, ctypes.c_void_p))
    imageView = UIImageView.alloc().initWithImage_(image)

    ciImage = CIImage.alloc().initWithImage_(imageView.image)
    #pdbr.state(image)
    imRef = CGDataProviderCopyData(CGImageGetDataProvider(image.CGImage))
    ciRef = CGDataProviderCopyData(CGImageGetDataProvider(ciImage.CGImage))
    
    #print(f'{imRef=}')
    #print(f'{ciRef=}')
    print(imRef)
    print(ciRef)
    

    self.view.addSubview_(imageView)
    imageView.translatesAutoresizingMaskIntoConstraints = False
    areaLayoutGuide = self.view.safeAreaLayoutGuide
    # --- imageView
    NSLayoutConstraint.activateConstraints_([
      imageView.centerXAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerXAnchor),
      imageView.centerYAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerYAnchor),
      imageView.leadingAnchor.constraintEqualToAnchor_constant_(
        areaLayoutGuide.leadingAnchor, 24.0),
      imageView.trailingAnchor.constraintEqualToAnchor_constant_(
        areaLayoutGuide.trailingAnchor, -24.0),
    ])

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

