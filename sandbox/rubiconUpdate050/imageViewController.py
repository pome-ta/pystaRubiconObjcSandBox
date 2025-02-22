'''
  note: Storyboard 未定義
'''
from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGRect

from pyLocalizedString import localizedString
from rbedge import pdbr

from rbedge.enumerations import (
  UIViewAutoresizing,
  UIViewContentMode,
)
from rbedge.pythonProcessUtils import dataWithContentsOfURL

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UIImageView = ObjCClass('UIImageView')
UIImage = ObjCClass('UIImage')
NSURL = ObjCClass('NSURL')
UIToolTipInteraction = ObjCClass('UIToolTipInteraction')

UIColor = ObjCClass('UIColor')


class ImageViewController(UIViewController):

  # MARK: - View Life Cycle
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.navigationItem.title = localizedString('ImageViewTitle') if (
      title := self.navigationItem.title) is None else title

    self.view.backgroundColor = UIColor.systemBackgroundColor()
    #self.view.backgroundColor = UIColor.systemIndigoColor()

    imageView = UIImageView.alloc().init()
    #imageView.backgroundColor = UIColor.systemOrangeColor()

    # --- Layout
    self.view.addSubview_(imageView)
    imageView.translatesAutoresizingMaskIntoConstraints = False
    #areaLayoutGuide = self.view.safeAreaLayoutGuide
    areaLayoutGuide = self.view
    NSLayoutConstraint.activateConstraints_([
      imageView.centerXAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerXAnchor),
      imageView.centerYAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerYAnchor),
      imageView.widthAnchor.constraintEqualToAnchor_multiplier_(
        areaLayoutGuide.widthAnchor, 1.0),
      imageView.heightAnchor.constraintEqualToAnchor_multiplier_(
        areaLayoutGuide.heightAnchor, 1.0),
    ])

    self.imageView = imageView
    self.configureImageView()

  # MARK: - Configuration
  @objc_method
  def configureImageView(self):
    # The root view of the view controller is set in Interface Builder and is an UIImageView.
    # ビュー コントローラーのルート ビューは Interface Builder で設定され、UIImageView です。
    # todo: 上記コメントと実装方法が違う。`self.imageView` は`self.view` で`addSubview_` してる。
    if (imageView := self.imageView).isKindOfClass_(UIImageView):
      # xxx: `lambda` の使い方が悪い
      flowers_str = lambda index: f'./UIKitCatalogCreatingAndCustomizingViewsAndControls/UIKitCatalog/Assets.xcassets/Flowers_{index}.imageset/Flowers_{index}.png'

      # Fetch the images (each image is of the format Flowers_number).
      self.imageView.animationImages = [
        UIImage.alloc().initWithData_scale_(
          dataWithContentsOfURL(flowers_str(i)), 1) for i in range(1, 3)
      ]
      # We want the image to be scaled to the correct aspect ratio within imageView's bounds.
      self.imageView.contentMode = UIViewContentMode.scaleAspectFit

      self.imageView.animationDuration = 5
      self.imageView.startAnimating()

      self.imageView.isAccessibilityElement = True
      self.imageView.accessibilityLabel = localizedString('Animated')

      if True:  # wip: `available(iOS 15, *)`
        interaction = UIToolTipInteraction.alloc().initWithDefaultToolTip_(
          localizedString('ImageToolTipTitle'))
        self.imageView.addInteraction_(interaction)


if __name__ == '__main__':
  from rbedge.functions import NSStringFromClass
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController

  main_vc = ImageViewController.new()
  _title = NSStringFromClass(ImageViewController)
  main_vc.navigationItem.title = _title

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  #style = UIModalPresentationStyle.popover

  present_viewController(main_vc, style)

