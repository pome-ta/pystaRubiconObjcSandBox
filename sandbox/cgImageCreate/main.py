import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
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

width_size: int = 40
height_size: int = 24


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
      UIColor.cyanColor.setFill()
      # todo: 色付けないとモノクロになる
      UIColor.systemBackgroundColor().setFill()
      context.fillRect_(renderer.format.bounds)

    image = renderer.imageWithActions_(
      Block(imageRendererContext, None, ctypes.c_void_p))
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
    #pdbr.state(CGImageGetDataProvider(self.imageView.image.CGImage))
    imageRef.replaceBytesInRange_withBytes_(NSRange(0, 4), bytes(vals))
    #imageRef.resetBytesInRange_(NSRange(4,24))
    imageRef.release()

    #pdbr.state(imageRef)
    #imageRef.setData_(bytes(vals * int(imageRef.length / 4)))

    #print(imageRef)
    #print(f'{imageRef=}')
    #print(imageRef)
    #print(dir(imageRef.bytes))
    #id = ctypes.byref(imageRef.bytes)
    #print(id)
    '''
    byref = ctypes.byref(imageRef.bytes)
    print(byref)
    print(dir(byref))
    print(byref.contents)
    '''

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

