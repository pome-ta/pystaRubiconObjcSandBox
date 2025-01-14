'''
  note: objc_util でやってみる
'''
import os
import ctypes
import ctypes.util
#from ctypes import util
from enum import IntEnum, auto
from objc_util import ObjCClass, ObjCInstance, create_objc_class, on_main_thread
from objc_util import sel, CGRect, ns, NSDictionary

import pdbg

_lib_path = ['/usr/lib']
_framework_path = ['/System/Library/Frameworks']


def load_library(name):
  path = ctypes.util.find_library(name)
  if path is not None:
    return ctypes.CDLL(path)

  for loc in _lib_path:
    try:
      return ctypes.CDLL(os.path.join(loc, "lib" + name + ".dylib"))
    except OSError:
      pass

  for loc in _framework_path:
    try:
      return ctypes.CDLL(os.path.join(loc, name + ".framework", name))
    except OSError:
      pass

  raise ValueError(f"Library {name!r} not found")


UIKit = load_library('UIKit')
NSForegroundColorAttributeName = ObjCInstance(
  ctypes.c_void_p.in_dll(UIKit, 'NSForegroundColorAttributeName'))

# --- navigation
UINavigationController = ObjCClass('UINavigationController')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

# --- viewController
UIViewController = ObjCClass('UIViewController')

# --- view
UIView = ObjCClass('UIView')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UIColor = ObjCClass('UIColor')
UIPickerView = ObjCClass('UIPickerView')
NSMutableAttributedString = ObjCClass('NSMutableAttributedString')


class RGB:
  max: float = 255.0
  min: float = 0.0
  offset: float = 5.0


class ColorComponent(IntEnum):
  red = 0
  green = auto()
  blue = auto()


class CustomViewController:

  def __init__(self):
    self._viewController: UIViewController
    self.nav_title = 'UIPickerView'

    self.numberOfColorValuesPerComponent = int(RGB.max / RGB.offset) + 1

    self.redColor = RGB.min
    self.greenColor = RGB.min
    self.blueColor = RGB.min

    self.colorSwatchPickerView = UIPickerView.new()
    self.colorSwatchView = UIView.alloc()

  def setup_viewDidLoad(self, this: UIViewController):
    # xxx: `viewDidLoad` が肥大化しそうなので、レイアウト関係以外はこっちで処理

    navigationItem = this.navigationItem()
    navigationItem.setTitle_(self.nav_title)

    # --- view
    CGRectZero = CGRect((0.0, 0.0), (0.0, 0.0))
    self.colorSwatchView.initWithFrame_(CGRectZero)
    #self.colorSwatchView.setBackgroundColor_(UIColor.systemRedColor())

  def configurePickerView(self):
    selectedRows = {
      ColorComponent.red: 13,
      ColorComponent.green: 41,
      ColorComponent.blue: 24,
    }
    for colorComponent, selectedRow in selectedRows.items():
      self.colorSwatchPickerView.selectRow_inComponent_animated_(
        selectedRow, int(colorComponent), True)

  def _override_viewController(self):

    # --- `UIViewController` Methods
    def viewDidLoad(_self, _cmd):
      this = ObjCInstance(_self)
      self.setup_viewDidLoad(this)
      view = this.view()

      # --- layout
      view.addSubview_(self.colorSwatchPickerView)
      self.colorSwatchPickerView.translatesAutoresizingMaskIntoConstraints = False
      view.addSubview_(self.colorSwatchView)
      self.colorSwatchView.translatesAutoresizingMaskIntoConstraints = False

      safeAreaLayoutGuide = view.safeAreaLayoutGuide()
      layoutMarginsGuide = view.layoutMarginsGuide()

      NSLayoutConstraint.activateConstraints_([
        self.colorSwatchPickerView.widthAnchor().constraintEqualToConstant_(
          375.0),
      ])

      NSLayoutConstraint.activateConstraints_([
        self.colorSwatchView.trailingAnchor().
        constraintEqualToAnchor_constant_(safeAreaLayoutGuide.trailingAnchor(),
                                          -20.0),
        self.colorSwatchView.topAnchor().constraintEqualToAnchor_constant_(
          self.colorSwatchPickerView.bottomAnchor(), 8.0),
        self.colorSwatchView.bottomAnchor().constraintEqualToAnchor_constant_(
          safeAreaLayoutGuide.bottomAnchor(), -20.0),
        self.colorSwatchPickerView.centerXAnchor().constraintEqualToAnchor_(
          safeAreaLayoutGuide.centerXAnchor()),
        self.colorSwatchPickerView.topAnchor(
        ).constraintEqualToAnchor_constant_(safeAreaLayoutGuide.topAnchor(),
                                            13.0),
        self.colorSwatchView.leadingAnchor().constraintEqualToAnchor_constant_(
          safeAreaLayoutGuide.leadingAnchor(), 20.0),
        self.colorSwatchPickerView.centerYAnchor().constraintEqualToAnchor_(
          safeAreaLayoutGuide.centerYAnchor()),
      ])

      self.configurePickerView()

    # --- `UIViewController` set up
    _methods = [
      viewDidLoad,
    ]

    create_kwargs = {
      'name': '_vc',
      'superclass': UIViewController,
      'methods': _methods,
    }
    _vc = create_objc_class(**create_kwargs)
    self._viewController = _vc

  def createUIPickerViewDataSource(self):

    def numberOfComponentsInPickerView_(_self, _cmd, pickerView):
      return len(ColorComponent)

    def pickerView_numberOfRowsInComponent_(_self, _cmd, pickerView,
                                            component):
      return self.numberOfColorValuesPerComponent

    # --- `UIPickerViewDataSource` set up
    _methods = [
      numberOfComponentsInPickerView_,
      pickerView_numberOfRowsInComponent_,
    ]
    _protocols = [
      'UIPickerViewDataSource',
    ]

    create_kwargs = {
      'name': '_dataSource',
      'methods': _methods,
      'protocols': _protocols,
    }
    _dataSource = create_objc_class(**create_kwargs)
    return _dataSource.new()

  def createUIPickerViewDelegate(self):

    def pickerView_attributedTitleForRow_forComponent_(_self, _cmd, pickerView,
                                                       row, component):

      colorValue = row * RGB.offset
      # Set the initial colors for each picker segment.
      value = colorValue / RGB.max
      redColorComponent = RGB.min
      greenColorComponent = RGB.min
      blueColorComponent = RGB.min

      if component == ColorComponent.red:
        redColorComponent = value
      if component == ColorComponent.green:
        greenColorComponent = value
      if component == ColorComponent.blue:
        blueColorComponent = value

      if redColorComponent < 0.5:
        redColorComponent = 0.5
      if blueColorComponent < 0.5:
        blueColorComponent = 0.5
      if greenColorComponent < 0.5:
        greenColorComponent = 0.5

      foregroundColor = UIColor.colorWithRed_green_blue_alpha_(
        redColorComponent, greenColorComponent, blueColorComponent, 1.0)

      attributes = NSDictionary.dictionaryWithObject(
        foregroundColor, forKey=NSForegroundColorAttributeName)

      title = NSMutableAttributedString.alloc().initWithString_attributes_(
        f'{int(colorValue)}', attributes)

      return title.ptr

    def pickerView_titleForRow_forComponent_(_self, _cmd, pickerView, row,
                                             component):
      colorValue = row * RGB.offset
      return ns(f'{int(colorValue)}').ptr

    # --- `UIPickerViewDelegate` set up
    _methods = [
      pickerView_attributedTitleForRow_forComponent_,
      #pickerView_titleForRow_forComponent_,
    ]
    _protocols = [
      'UIPickerViewDelegate',
    ]

    create_kwargs = {
      'name': '_delegate',
      'methods': _methods,
      'protocols': _protocols,
    }
    _delegate = create_objc_class(**create_kwargs)
    return _delegate.new()

  #@on_main_thread
  def _init(self):
    self._override_viewController()
    vc = self._viewController.new().autorelease()
    _dataSource = self.createUIPickerViewDataSource()
    _delegate = self.createUIPickerViewDelegate()
    self.colorSwatchPickerView.setDataSource_(_dataSource)
    self.colorSwatchPickerView.setDelegate_(_delegate)
    return vc

  @classmethod
  def new(cls) -> ObjCInstance:
    _cls = cls()
    return _cls._init()


class ObjcUIViewController:

  def __init__(self):
    self._navigationController: UINavigationController

  def _override_navigationController(self):
    # --- `UINavigationController` Methods
    def closeButtonTapped_(_self, _cmd, _sender):
      this = ObjCInstance(_self)
      visibleViewController = this.visibleViewController()
      visibleViewController.dismissViewControllerAnimated_completion_(
        True, None)

    # --- `UINavigationController` set up
    _methods = [
      closeButtonTapped_,
    ]

    create_kwargs = {
      'name': '_nv',
      'superclass': UINavigationController,
      'methods': _methods,
    }
    _nv = create_objc_class(**create_kwargs)
    self._navigationController = _nv

  def create_navigationControllerDelegate(self):
    # --- `UINavigationControllerDelegate` Methods
    def navigationController_willShowViewController_animated_(
        _self, _cmd, _navigationController, _viewController, _animated):

      navigationController = ObjCInstance(_navigationController)
      viewController = ObjCInstance(_viewController)

      # --- appearance
      '''
      appearance = UINavigationBarAppearance.alloc()
      appearance.configureWithDefaultBackground()
      #appearance.configureWithOpaqueBackground()
      #appearance.configureWithTransparentBackground()
      #appearance.backgroundColor = sc.systemExtraLightGrayColor

      # --- navigationBar
      navigationBar = navigationController.navigationBar()

      navigationBar.standardAppearance = appearance
      navigationBar.scrollEdgeAppearance = appearance
      navigationBar.compactAppearance = appearance
      navigationBar.compactScrollEdgeAppearance = appearance

      #navigationBar.prefersLargeTitles = True
      '''

      viewController.setEdgesForExtendedLayout_(0)
      #viewController.setExtendedLayoutIncludesOpaqueBars_(True)

      _close_btn = UIBarButtonItem.alloc()
      close_btn = _close_btn.initWithBarButtonSystemItem_target_action_(
        24, navigationController, sel('closeButtonTapped:'))

      visibleViewController = navigationController.visibleViewController()

      # --- navigationItem
      navigationItem = visibleViewController.navigationItem()

      #navigationItem.setTitle_('nv')
      navigationItem.rightBarButtonItem = close_btn

    # --- `UINavigationControllerDelegate` set up
    _methods = [
      navigationController_willShowViewController_animated_,
    ]
    _protocols = [
      'UINavigationControllerDelegate',
    ]

    create_kwargs = {
      'name': '_nvDelegate',
      'methods': _methods,
      'protocols': _protocols,
    }
    _nvDelegate = create_objc_class(**create_kwargs)
    return _nvDelegate.new()

  @on_main_thread
  def _init(self, vc: UIViewController):
    self._override_navigationController()
    _delegate = self.create_navigationControllerDelegate()
    nv = self._navigationController.alloc()
    nv.initWithRootViewController_(vc).autorelease()
    nv.setDelegate_(_delegate)
    return nv

  @classmethod
  def new(cls, vc: UIViewController) -> ObjCInstance:
    _cls = cls()
    return _cls._init(vc)


@on_main_thread
def present_objc(vc):
  app = ObjCClass('UIApplication').sharedApplication()
  window = app.keyWindow() if app.keyWindow() else app.windows().firstObject()

  root_vc = window.rootViewController()

  while root_vc.presentedViewController():
    root_vc = root_vc.presentedViewController()
  '''
  case -2 : automatic
  case -1 : none
  case  0 : fullScreen
  case  1 : pageSheet <- default ?
  case  2 : formSheet
  case  3 : currentContext
  case  4 : custom
  case  5 : overFullScreen
  case  6 : overCurrentContext
  case  7 : popover
  case  8 : blurOverFullScreen
  '''
  vc.setModalPresentationStyle(0)
  root_vc.presentViewController_animated_completion_(vc, True, None)


if __name__ == '__main__':
  cvc = CustomViewController.new()
  ovc = ObjcUIViewController.new(cvc)
  present_objc(ovc)

