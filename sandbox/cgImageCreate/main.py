import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSizeMake, NSRange

from rbedge.functions import (
  NSStringFromClass,
  CGImageGetDataProvider,
  CGDataProviderCopyData,
)

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
UIColor = ObjCClass('UIColor')

UIGraphicsImageRenderer = ObjCClass('UIGraphicsImageRenderer')
UIImageView = ObjCClass('UIImageView')

width_size: int = 29
height_size: int = 32



class MainViewController(UIViewController):

  imageView: UIImageView = objc_property()

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

    _size = CGSizeMake(width_size, height_size)
    renderer = UIGraphicsImageRenderer.alloc().initWithSize_(_size)

    #pdbr.state(renderer.format)

    def imageRendererContext(_context: ctypes.c_void_p) -> None:
      context = ObjCInstance(_context)
      #65536:5e5ce6ff
      #UIColor.systemIndigoColor().setFill()
      #32768:ffffffff
      #UIColor.whiteColor.setFill()
      #65536:ffff00ff
      #UIColor.yellowColor.setFill()
      #65536:64d2ffff
      #UIColor.systemCyanColor().setFill()
      #32768:00ffffff
      UIColor.cyanColor.setFill()
      #32768:80ff80ff
      #UIColor.grayColor.setFill()
      #32768:55ff55ff
      #UIColor.darkGrayColor.setFill()
      #32768:aaffaaff
      #UIColor.lightGrayColor.setFill()
      #32768:00ff00ff
      #UIColor.blackColor.setFill()

      #32768:00ff00ff
      context.fillRect_(renderer.format.bounds)
      #pdbr.state(context.format)

    image = renderer.imageWithActions_(
      Block(imageRendererContext, None, ctypes.c_void_p))
    #pdbr.state(renderer.format)
    #print(renderer.format.preferredRange)
    #pdbr.state(image)
    # todo: 空撃ち
    #32768:00000000
    #image = renderer.imageWithActions_(Block(lambda context: None, None, ctypes.c_void_p))
    imageView = UIImageView.alloc().initWithImage_(image)

    self.view.addSubview_(imageView)

    imageView.translatesAutoresizingMaskIntoConstraints = False
    areaLayoutGuide = self.view.safeAreaLayoutGuide
    # --- imageView
    NSLayoutConstraint.activateConstraints_([
      imageView.centerXAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerXAnchor),
      imageView.centerYAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerYAnchor),

      #imageView.leadingAnchor.constraintEqualToAnchor_constant_(areaLayoutGuide.leadingAnchor, 24.0),
      #imageView.trailingAnchor.constraintEqualToAnchor_constant_(areaLayoutGuide.trailingAnchor, -24.0),
      imageView.widthAnchor.constraintEqualToAnchor_multiplier_(
        areaLayoutGuide.widthAnchor, 0.5),
      imageView.heightAnchor.constraintEqualToAnchor_multiplier_(
        areaLayoutGuide.widthAnchor, 0.5),
    ])

    self.imageView = imageView

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewWillAppear_')
    imageRef = CGDataProviderCopyData(
      CGImageGetDataProvider(self.imageView.image.CGImage))

    #print(f'{imageRef=}')

    #print(f'{imageRef=}')
    #print(imageRef)

    #pdbr.state(imageRef)
    #print(imageRef.bytes)
    #print(imageRef.mutableBytes)
    #print(imageRef.length)
    # 94 : 5e
    # 92 : 5c
    #230 : e6
    vals = [94, 92, 230, 255]  # * int(imageRef.length / 4)
    '''
    for i in range(int(imageRef.length / 4)):
      if i % 2 == 0:
        continue
      #vals = [94, 92, 230, 255]

      imageRef.replaceBytesInRange_withBytes_(NSRange(i * 4, 4), bytes(vals))
    '''
    #imageRef.replaceBytesInRange_withBytes_(NSRange(0, 4), bytes(vals))
    imageRef.resetBytesInRange_(NSRange(4,24))
    
    #pdbr.state(imageRef)
    #imageRef.setData_(bytes(vals * int(imageRef.length / 4)))

    #print(imageRef)
    #print(f'{imageRef=}')
    #print(imageRef)

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewDidAppear_')

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

