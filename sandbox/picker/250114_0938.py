'''
  note: Storyboard 実装なし
'''
import ctypes
from enum import IntEnum, auto

from pyrubicon.objc.api import ObjCClass, ObjCInstance, ObjCProtocol, NSString
from pyrubicon.objc.api import objc_method, objc_rawmethod, ns_from_py, py_from_ns
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.collections import ObjCStrInstance

from rbedge.enumerations import (
  UILayoutConstraintAxis,
  UIUserInterfaceSizeClass,
  UIDatePickerStyle,
  NSDateFormatterStyle,
  NSCalendarUnit,
  UIControlEvents,
  NSTextAlignment,
  NSLineBreakMode,
)

from rbedge.globalVariables import (
  NSAttributedStringKey, )

from rbedge import pdbr
#from pyLocalizedString import localizedString

#UIKit = load_library('UIKit')  # todo: `objc_const` 用
UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
UIColor = ObjCClass('UIColor')
NSDictionary = ObjCClass('NSDictionary')

UIPickerView = ObjCClass('UIPickerView')
UIView = ObjCClass('UIView')
NSMutableAttributedString = ObjCClass('NSMutableAttributedString')
NSAttributedString = ObjCClass('NSAttributedString')
UILabel = ObjCClass('UILabel')
UIFont = ObjCClass('UIFont')
CIColor = ObjCClass('CIColor')

UIPickerViewDataSource = ObjCProtocol('UIPickerViewDataSource')
UIPickerViewDelegate = ObjCProtocol('UIPickerViewDelegate')



class RGB:
  max: float = 255.0
  min: float = 0.0
  offset: float = 5.0


class ColorComponent(IntEnum):
  red = 0
  green = auto()
  blue = auto()

'''
class PickerViewController(UIViewController,
                           protocols=[
                             UIPickerViewDataSource,
                             UIPickerViewDelegate,
                           ]):
'''
class PickerViewController(UIViewController):
  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print('\tdealloc')
    pass

  # MARK: - View Life Cycle
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.navigationItem.title = 'PickerViewTitle' if (
      title := self.navigationItem.title) is None else title
    #self.view.backgroundColor = UIColor.systemBackgroundColor()

    # --- pickerView
    # todo: 変数名`pickerView` だと、関数名に干渉する
    colorSwatchPickerView = UIPickerView.new()
    colorSwatchPickerView.dataSource = self
    colorSwatchPickerView.delegate = self

    #pdbr.state(colorSwatchPickerView.dataSource)

    # --- Layout
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide
    layoutMarginsGuide = self.view.layoutMarginsGuide

    self.view.addSubview_(colorSwatchPickerView)
    colorSwatchPickerView.translatesAutoresizingMaskIntoConstraints = False

    NSLayoutConstraint.activateConstraints_([
      colorSwatchPickerView.widthAnchor.constraintEqualToConstant_(375.0),
    ])

    NSLayoutConstraint.activateConstraints_([
      colorSwatchPickerView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      colorSwatchPickerView.topAnchor.constraintEqualToAnchor_constant_(
        safeAreaLayoutGuide.topAnchor, 13.0),
    ])

    self.colorSwatchPickerView = colorSwatchPickerView

    self.numberOfColorValuesPerComponent = 2#int(RGB.max / RGB.offset) + 1

    self.redColor = RGB.min
    self.greenColor = RGB.min
    self.blueColor = RGB.min

    self.configurePickerView()

  @objc_method
  def configurePickerView(self):
    # Set the default selected rows (the desired rows to initially select will vary from app to app).
    # デフォルトの選択行を設定します (最初に選択する行はアプリによって異なります)。
    selectedRows = {
      ColorComponent.red: 13,
      ColorComponent.green: 41,
      ColorComponent.blue: 24,
    }

    for colorComponent, selectedRow in selectedRows.items():
      """
      Note that the delegate method on `UIPickerViewDelegate` is not triggered
      when manually calling `selectRow(_:inComponent:animated:)`. To do
      this, we fire off delegate method manually.
      """
      """
      `selectRow(_:inComponent:animated:)` を手動で呼び出した場合、`UIPickerViewDelegate` のデリゲート メソッドはトリガーされないことに注意してください。これを行うには、デリゲート メソッドを手動で起動します。
      """
      self.colorSwatchPickerView.selectRow_inComponent_animated_(
        selectedRow, int(colorComponent), True)
      #self.pickerView(self.colorSwatchPickerView,didSelectRow=selectedRow,inComponent=int(colorComponent))

  # MARK: - UIPickerViewDataSource
  @objc_method
  def numberOfComponentsInPickerView_(self, pickerView) -> int:
    return len(ColorComponent)
    #return 1

  @objc_method
  def pickerView_numberOfRowsInComponent_(self, component) -> int:
    #print(component)
    return self.numberOfColorValuesPerComponent

  # MARK: - UIPickerViewDelegate
  @objc_rawmethod
  def pickerView_attributedTitleForRow_forComponent_(self, _cmd, pickerView, row:int,
                                           component):
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
    
    #print(ctypes.c_byte(NSAttributedStringKey.foregroundColor))
    #pdbr.state(foregroundColor.cgColor())
    attributes = NSDictionary.dictionaryWithObject(foregroundColor, forKey=NSAttributedStringKey.foregroundColor)
    #print(attributes)
    #attributes = {}
    title = NSMutableAttributedString.alloc().initWithString_attributes_(f'{int(colorValue)}', attributes)
    print(title)
    #return ctypes.pointer(title)
    #return 0
    return title.ptr

  @objc_method
  def pickerView_titleForRow_forComponent_(self, pickerView, row: int,
                                           component: int) -> objc_id:
    colorValue = row * RGB.offset
    return f'{int(colorValue)}'
    

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewWillAppear')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewDidAppear')
    #pdbr.state(self, 1)

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewDidDisappear')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'{__class__}: didReceiveMemoryWarning')


if __name__ == '__main__':
  from rbedge.functions import NSStringFromClass
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController

  main_vc = PickerViewController.new()

  _title = NSStringFromClass(PickerViewController)
  main_vc.navigationItem.title = _title

  presentation_style = UIModalPresentationStyle.fullScreen
  present_viewController(main_vc, presentation_style)

